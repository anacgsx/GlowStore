from decimal import Decimal


class CartCalculator:
    """Microsserviço lógico responsável por cálculos simples do carrinho."""

    @staticmethod
    def item_total(price: Decimal, quantity: int) -> Decimal:
        return (price * quantity).quantize(Decimal("0.01"))

    @staticmethod
    def subtotal(items) -> Decimal:
        return sum((item["total"] for item in items), Decimal("0.00")).quantize(Decimal("0.01"))
