import os
import sys
import django
from decimal import Decimal
from uuid import uuid4

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glowstore.settings")
django.setup()

from behave import given, when, then
from django.contrib.auth.models import User
from django.test import Client

from servico_pagamentos import PixPayment
from servico_GlowClub import GlowClubService

from store.models import (
    BeautyStore,
    Category,
    Product,
    Order,
    GlowClubAccount,
    GlowReward,
)


@given("que existe um produto disponível na GlowStore")
def step_produto_disponivel(context):
    suffix = uuid4().hex[:8]

    context.store = BeautyStore.objects.create(
        name=f"Ruby Rose Teste {suffix}",
        slogan="Beauty with you",
        description="Loja criada para teste BDD.",
        is_featured=True,
    )

    context.category = Category.objects.create(
        name=f"Make Teste {suffix}",
        description="Categoria criada para teste BDD.",
    )

    context.product = Product.objects.create(
        store=context.store,
        category=context.category,
        name=f"Lip Gloss Teste {suffix}",
        description="Produto criado para teste BDD.",
        price=Decimal("50.00"),
        stock=10,
        is_trending=True,
    )

    context.client = Client()


@when("o cliente clica em adicionar ao carrinho")
def step_cliente_adiciona_carrinho(context):
    session = context.client.session
    session["cart"] = {
        str(context.product.id): 1
    }
    session.save()


@then("o produto deve aparecer no carrinho")
def step_produto_aparece_carrinho(context):
    cart = context.client.session.get("cart", {})

    assert str(context.product.id) in cart
    assert cart[str(context.product.id)] == 1


@then("o subtotal deve ser calculado corretamente")
def step_subtotal_calculado(context):
    cart = context.client.session.get("cart", {})
    quantity = cart[str(context.product.id)]

    subtotal = context.product.price * quantity

    assert subtotal == Decimal("50.00")


@given("que o carrinho possui produtos")
def step_carrinho_possui_produtos(context):
    context.subtotal = Decimal("100.00")


@when("o cliente escolhe Pix")
def step_cliente_escolhe_pix(context):
    payment = PixPayment()

    context.discount = payment.apply_discount(context.subtotal)
    context.total = context.subtotal - context.discount


@then("o checkout deve aplicar desconto de 5 por cento")
def step_checkout_desconto_pix(context):
    assert context.discount == Decimal("5.00")


@then("o total deve ser atualizado na tela")
def step_total_atualizado(context):
    assert context.total == Decimal("95.00")


@given("que o cliente finalizou um pedido pago")
def step_cliente_finalizou_pedido(context):
    suffix = uuid4().hex[:8]

    context.user = User.objects.create_user(
        username=f"cliente_bdd_{suffix}",
        email=f"cliente_bdd_{suffix}@teste.com",
        password="123456",
    )

    context.order = Order.objects.create(
        user=context.user,
        full_name="Cliente BDD",
        address="Rua de Teste, 123",
        payment_method="pix",
        shipping_method="standard",
        subtotal=Decimal("100.00"),
        shipping_total=Decimal("0.00"),
        discount_total=Decimal("0.00"),
        total=Decimal("100.00"),
        status="paid",
    )


@when("o pedido é confirmado")
def step_pedido_confirmado(context):
    context.account = GlowClubService.add_points_for_order(context.order)


@then("o sistema deve adicionar 1 ponto a cada R$1 gasto")
def step_adiciona_pontos_por_real(context):
    context.account.refresh_from_db()

    assert context.account.points == 100
    assert context.account.lifetime_points == 100


@then("os pontos devem aparecer no perfil do cliente")
def step_pontos_aparecem_perfil(context):
    account = GlowClubAccount.objects.get(user=context.user)

    assert account.points == 100


@given("que o cliente possui pontos suficientes")
def step_cliente_possui_pontos(context):
    suffix = uuid4().hex[:8]

    context.user = User.objects.create_user(
        username=f"cliente_resgate_{suffix}",
        email=f"cliente_resgate_{suffix}@teste.com",
        password="123456",
    )

    context.account = GlowClubAccount.objects.create(
        user=context.user,
        points=200,
        lifetime_points=200,
    )

    context.reward = GlowReward.objects.create(
        title=f"R$10 OFF Teste {suffix}",
        description="Cupom de desconto criado para teste BDD.",
        points_required=150,
        reward_type=GlowReward.DISCOUNT,
        discount_value=Decimal("10.00"),
        is_active=True,
    )


@when("ele resgata uma recompensa")
def step_resgata_recompensa(context):
    context.redemption = GlowClubService.redeem(
        user=context.user,
        reward=context.reward,
    )


@then("o sistema deve gerar um código GlowClub")
def step_gera_codigo_glowclub(context):
    assert context.redemption.code.startswith("GLOW-")
    assert len(context.redemption.code) > 5


@then("os pontos usados devem ser removidos do saldo")
def step_remove_pontos_usados(context):
    context.account.refresh_from_db()

    assert context.account.points == 50