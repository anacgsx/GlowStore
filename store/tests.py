from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from servico_GlowClub import GlowClubService
from .models import GlowReward, Order
from .patterns import OrderBuilder, PaymentStrategyFactory, ShippingStrategyFactory


class PaymentServiceTests(TestCase):
    def test_pix_payment_applies_five_percent_discount(self):
        payment = PaymentStrategyFactory.create('pix')
        self.assertEqual(payment.apply_discount(Decimal('100.00')), Decimal('5.00'))

    def test_unknown_payment_falls_back_to_credit_card(self):
        payment = PaymentStrategyFactory.create('unknown')
        self.assertEqual(payment.label, 'Cartão de crédito')


class ShippingServiceTests(TestCase):
    def test_standard_shipping_is_free_after_minimum_subtotal(self):
        shipping = ShippingStrategyFactory.create('standard')
        self.assertEqual(shipping.calculate(Decimal('180.00')), Decimal('0.00'))

    def test_express_shipping_has_fixed_price(self):
        shipping = ShippingStrategyFactory.create('express')
        self.assertEqual(shipping.calculate(Decimal('80.00')), Decimal('29.90'))


class OrderBuilderTests(TestCase):
    def test_builder_calculates_total(self):
        user = User.objects.create_user(username='ana')
        draft = (
            OrderBuilder()
            .with_customer(user, 'Ana Carolina', 'Rua Glow, 123')
            .with_cart([], Decimal('200.00'))
            .with_payment('pix', Decimal('10.00'), '')
            .with_shipping('standard', Decimal('0.00'))
            .build()
        )
        self.assertEqual(draft.total, Decimal('190.00'))


class GlowClubServiceTests(TestCase):
    def test_order_generates_one_point_per_real(self):
        user = User.objects.create_user(username='cliente')
        order = Order.objects.create(
            user=user,
            full_name='Cliente Glow',
            address='Rua Teste, 100',
            payment_method='pix',
            shipping_method='standard',
            subtotal=Decimal('100.00'),
            shipping_total=Decimal('0.00'),
            discount_total=Decimal('5.00'),
            total=Decimal('95.00'),
        )
        account = GlowClubService.add_points_for_order(order)
        order.refresh_from_db()
        self.assertEqual(account.points, 95)
        self.assertEqual(order.glow_points_earned, 95)

    def test_user_can_redeem_reward_when_has_enough_points(self):
        user = User.objects.create_user(username='cliente')
        account = GlowClubService.account_for(user)
        account.points = 200
        account.save()
        reward = GlowReward.objects.create(
            title='R$10 OFF',
            description='Cupom teste',
            points_required=150,
            reward_type='discount',
            discount_value=Decimal('10.00'),
        )
        redemption = GlowClubService.redeem(user, reward)
        account.refresh_from_db()
        self.assertEqual(account.points, 50)
        self.assertTrue(redemption.code.startswith('GLOW-'))
