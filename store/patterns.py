from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import List
from django.contrib import messages
from servico_carrinho import CartCalculator
from servico_GlowClub import GlowClubService
from servico_pagamentos import PaymentStrategy, PaymentStrategyFactory
from .models import FavoriteProduct, FavoriteStore, Order, OrderItem, Product


# 1) SINGLETON
class CartSession:
    """Carrinho salvo na sessão do Django com uma única instância por request."""

    _instances = {}

    def __new__(cls, request):
        key = id(request)
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls)
        return cls._instances[key]

    def __init__(self, request):
        if getattr(self, '_ready', False):
            return
        self.request = request
        self.session = request.session
        self.cart = self.session.setdefault('cart', {})
        self._ready = True

    def add(self, product_id: int, quantity: int = 1):
        key = str(product_id)
        self.cart[key] = self.cart.get(key, 0) + max(quantity, 1)
        self.save()

    def remove(self, product_id: int):
        self.cart.pop(str(product_id), None)
        self.save()

    def clear(self):
        self.session['cart'] = {}
        self.cart = self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True

    def count(self) -> int:
        return sum(self.cart.values())

    def items(self):
        products = Product.objects.filter(id__in=self.cart.keys()).select_related('store', 'category')
        rows = []
        for product in products:
            quantity = self.cart[str(product.id)]
            rows.append({
                'product': product,
                'quantity': quantity,
                'total': CartCalculator.item_total(product.price, quantity),
            })
        return rows

    def subtotal(self) -> Decimal:
        return CartCalculator.subtotal(self.items())


# 2) STRATEGY DE ENTREGA
class ShippingStrategy(ABC):
    code = 'standard'
    label = 'Entrega'
    description = 'Forma de entrega da GlowStore'

    @abstractmethod
    def calculate(self, subtotal: Decimal) -> Decimal:
        pass


class StandardShipping(ShippingStrategy):
    code = 'standard'
    label = 'Entrega padrão'
    description = 'Frete grátis acima de R$180 ou R$18,90.'

    def calculate(self, subtotal: Decimal) -> Decimal:
        return Decimal('0.00') if subtotal >= Decimal('180.00') else Decimal('18.90')


class ExpressShipping(ShippingStrategy):
    code = 'express'
    label = 'Entrega expressa'
    description = 'Entrega mais rápida com taxa fixa.'

    def calculate(self, subtotal: Decimal) -> Decimal:
        return Decimal('29.90')


class PickupShipping(ShippingStrategy):
    code = 'pickup'
    label = 'Retirada na loja'
    description = 'Retirada sem custo em loja parceira.'

    def calculate(self, subtotal: Decimal) -> Decimal:
        return Decimal('0.00')


class ScheduledShipping(ShippingStrategy):
    code = 'scheduled'
    label = 'Entrega agendada'
    description = 'Entrega com janela agendada.'

    def calculate(self, subtotal: Decimal) -> Decimal:
        return Decimal('24.90')


class ShippingStrategyFactory:
    strategies = {
        StandardShipping.code: StandardShipping,
        ExpressShipping.code: ExpressShipping,
        PickupShipping.code: PickupShipping,
        ScheduledShipping.code: ScheduledShipping,
    }

    @classmethod
    def create(cls, method: str) -> ShippingStrategy:
        return cls.strategies.get(method, StandardShipping)()

    @classmethod
    def choices(cls):
        return [(code, strategy.label) for code, strategy in cls.strategies.items()]

    @classmethod
    def frontend_options(cls):
        options = []
        for code, strategy_class in cls.strategies.items():
            strategy = strategy_class()
            options.append({
                'code': code,
                'label': strategy.label,
                'description': strategy.description,
            })
        return options


class ShippingContext:
    def __init__(self, strategy: ShippingStrategy):
        self.strategy = strategy

    def total(self, subtotal: Decimal) -> Decimal:
        return self.strategy.calculate(subtotal)


# 3) BUILDER
@dataclass
class OrderDraft:
    user: object
    full_name: str
    address: str
    payment_method: str
    shipping_method: str
    reward_code: str
    subtotal: Decimal
    shipping_total: Decimal
    discount_total: Decimal
    total: Decimal
    items: List[dict]


class OrderBuilder:
    def __init__(self):
        self.data = {}

    def with_customer(self, user, full_name: str, address: str):
        self.data.update(user=user, full_name=full_name, address=address)
        return self

    def with_payment(self, payment_method: str, discount_total: Decimal, reward_code: str = ''):
        self.data.update(payment_method=payment_method, discount_total=discount_total, reward_code=reward_code)
        return self

    def with_shipping(self, shipping_method: str, shipping_total: Decimal):
        self.data.update(shipping_method=shipping_method, shipping_total=shipping_total)
        return self

    def with_cart(self, items: List[dict], subtotal: Decimal):
        self.data.update(items=items, subtotal=subtotal)
        return self

    def build(self) -> OrderDraft:
        total = self.data['subtotal'] + self.data['shipping_total'] - self.data['discount_total']
        self.data['total'] = max(total, Decimal('0.00')).quantize(Decimal('0.01'))
        return OrderDraft(**self.data)


# 4) OBSERVER
class OrderObserver(ABC):
    @abstractmethod
    def update(self, order: Order):
        pass


class DashboardObserver(OrderObserver):
    def update(self, order: Order):
        order.status = 'paid'
        order.save(update_fields=['status'])


class StockObserver(OrderObserver):
    def update(self, order: Order):
        for item in order.items.select_related('product'):
            product = item.product
            product.stock = max(product.stock - item.quantity, 0)
            product.save(update_fields=['stock'])


class GlowClubObserver(OrderObserver):
    def update(self, order: Order):
        GlowClubService.add_points_for_order(order)


class OrderSubject:
    def __init__(self):
        self.observers: List[OrderObserver] = []

    def attach(self, observer: OrderObserver):
        self.observers.append(observer)

    def notify(self, order: Order):
        for observer in self.observers:
            observer.update(order)


# 5) FACADE
class CheckoutFacade:
    def __init__(self, request):
        self.request = request
        self.cart = CartSession(request)

    def preview(self, payment_method='credit', shipping_method='standard', reward_code=''):
        subtotal = self.cart.subtotal()
        payment: PaymentStrategy = PaymentStrategyFactory.create(payment_method)
        shipping_strategy = ShippingStrategyFactory.create(shipping_method)
        shipping_total = ShippingContext(shipping_strategy).total(subtotal)
        payment_discount = payment.apply_discount(subtotal)
        reward_discount = Decimal('0.00')
        if self.request.user.is_authenticated:
            reward_discount = GlowClubService.available_discount(self.request.user, reward_code, subtotal)
        discount_total = (payment_discount + reward_discount).quantize(Decimal('0.01'))
        total = max(subtotal + shipping_total - discount_total, Decimal('0.00')).quantize(Decimal('0.01'))
        return {
            'subtotal': subtotal,
            'shipping_total': shipping_total,
            'payment_discount': payment_discount,
            'reward_discount': reward_discount,
            'discount_total': discount_total,
            'total': total,
            'payment_label': payment.label,
            'shipping_label': shipping_strategy.label,
        }

    def finish_order(self, full_name: str, address: str, payment_method: str, shipping_method: str, reward_code: str = '') -> Order:
        totals = self.preview(payment_method, shipping_method, reward_code)
        draft = (
            OrderBuilder()
            .with_customer(self.request.user, full_name, address)
            .with_cart(self.cart.items(), totals['subtotal'])
            .with_payment(payment_method, totals['discount_total'], reward_code)
            .with_shipping(shipping_method, totals['shipping_total'])
            .build()
        )
        order = Order.objects.create(
            user=draft.user,
            full_name=draft.full_name,
            address=draft.address,
            payment_method=draft.payment_method,
            shipping_method=draft.shipping_method,
            reward_code=draft.reward_code,
            subtotal=draft.subtotal,
            shipping_total=draft.shipping_total,
            discount_total=draft.discount_total,
            total=draft.total,
        )
        for item in draft.items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                unit_price=item['product'].price,
            )
        GlowClubService.use_discount_code(self.request.user, reward_code)
        subject = OrderSubject()
        subject.attach(DashboardObserver())
        subject.attach(StockObserver())
        subject.attach(GlowClubObserver())
        subject.notify(order)
        self.cart.clear()
        return order

    def frontend_config(self):
        subtotal = self.cart.subtotal()
        return {
            'subtotal': float(subtotal),
            'payments': PaymentStrategyFactory.frontend_options(),
            'shippings': ShippingStrategyFactory.frontend_options(),
            'standard_free_from': 180.0,
        }


# 6) COMMAND
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class AddToCartCommand(Command):
    def __init__(self, request, product: Product, quantity: int = 1):
        self.request = request
        self.product = product
        self.quantity = quantity

    def execute(self):
        CartSession(self.request).add(self.product.id, self.quantity)
        messages.success(self.request, f'{self.product.name} foi para sua necessaire 🛍️')


class ToggleFavoriteProductCommand(Command):
    def __init__(self, user, product: Product):
        self.user = user
        self.product = product

    def execute(self):
        favorite, created = FavoriteProduct.objects.get_or_create(user=self.user, product=self.product)
        if not created:
            favorite.delete()
        return created


class ToggleFavoriteStoreCommand(Command):
    def __init__(self, user, store):
        self.user = user
        self.store = store

    def execute(self):
        favorite, created = FavoriteStore.objects.get_or_create(user=self.user, store=self.store)
        if not created:
            favorite.delete()
        return created
