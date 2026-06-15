from abc import ABC, abstractmethod
from decimal import Decimal


class PaymentStrategy(ABC):
    """Contrato do microsserviço lógico de pagamentos."""

    code = "credit"
    label = "Pagamento"
    description = "Forma de pagamento da GlowStore"

    @abstractmethod
    def apply_discount(self, subtotal: Decimal) -> Decimal:
        """Retorna o desconto aplicado ao subtotal."""
        raise NotImplementedError


class PixPayment(PaymentStrategy):
    code = "pix"
    label = "Pix"
    description = "Aprovação imediata com 5% de desconto."

    def apply_discount(self, subtotal: Decimal) -> Decimal:
        return (subtotal * Decimal("0.05")).quantize(Decimal("0.01"))


class CreditCardPayment(PaymentStrategy):
    code = "credit"
    label = "Cartão de crédito"
    description = "Parcelamento simulado em até 6x sem desconto."

    def apply_discount(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")


class DebitCardPayment(PaymentStrategy):
    code = "debit"
    label = "Cartão de débito"
    description = "Pagamento à vista com 2% de desconto."

    def apply_discount(self, subtotal: Decimal) -> Decimal:
        return (subtotal * Decimal("0.02")).quantize(Decimal("0.01"))


class BankSlipPayment(PaymentStrategy):
    code = "boleto"
    label = "Boleto"
    description = "Pagamento via boleto com 3% de desconto."

    def apply_discount(self, subtotal: Decimal) -> Decimal:
        return (subtotal * Decimal("0.03")).quantize(Decimal("0.01"))


class PayPalPayment(PaymentStrategy):
    code = "paypal"
    label = "PayPal"
    description = "Carteira digital sem desconto adicional."

    def apply_discount(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")


class GlowClubPayment(PaymentStrategy):
    code = "club"
    label = "GlowClub"
    description = "Benefício de membro com 10% de desconto."

    def apply_discount(self, subtotal: Decimal) -> Decimal:
        return (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))


class PaymentStrategyFactory:
    """Factory responsável por criar a estratégia de pagamento correta."""

    strategies = {
        PixPayment.code: PixPayment,
        CreditCardPayment.code: CreditCardPayment,
        DebitCardPayment.code: DebitCardPayment,
        BankSlipPayment.code: BankSlipPayment,
        PayPalPayment.code: PayPalPayment,
        GlowClubPayment.code: GlowClubPayment,
    }

    @classmethod
    def create(cls, method: str) -> PaymentStrategy:
        strategy = cls.strategies.get(method, CreditCardPayment)
        return strategy()

    @classmethod
    def choices(cls):
        return [(code, strategy.label) for code, strategy in cls.strategies.items()]

    @classmethod
    def frontend_options(cls):
        options = []
        for code, strategy_class in cls.strategies.items():
            strategy = strategy_class()
            options.append({
                "code": code,
                "label": strategy.label,
                "description": strategy.description,
            })
        return options
