from decimal import Decimal
from django.utils.crypto import get_random_string
from django.utils import timezone


class GlowClubService:
    """Microsserviço lógico do programa de pontos GlowClub."""

    POINTS_PER_REAL = Decimal("1")

    @classmethod
    def account_for(cls, user):
        from store.models import GlowClubAccount
        account, _ = GlowClubAccount.objects.get_or_create(user=user)
        return account

    @classmethod
    def points_for_order(cls, amount: Decimal) -> int:
        return max(int(amount), 0)

    @classmethod
    def add_points_for_order(cls, order):
        from store.models import GlowClubTransaction
        account = cls.account_for(order.user)
        points = cls.points_for_order(order.total)
        if points <= 0:
            return account
        account.points += points
        account.lifetime_points += points
        account.save(update_fields=["points", "lifetime_points"])
        order.glow_points_earned = points
        order.save(update_fields=["glow_points_earned"])
        GlowClubTransaction.objects.create(
            account=account,
            points=points,
            reason=f"Pontos do pedido #{order.id}",
            order=order,
        )
        return account

    @classmethod
    def redeem(cls, user, reward):
        from store.models import GlowClubRedemption, GlowClubTransaction
        account = cls.account_for(user)
        if account.points < reward.points_required:
            raise ValueError("Pontos insuficientes para este resgate.")
        code = f"GLOW-{get_random_string(8).upper()}"
        account.points -= reward.points_required
        account.save(update_fields=["points"])
        redemption = GlowClubRedemption.objects.create(
            user=user,
            reward=reward,
            code=code,
            points_spent=reward.points_required,
        )
        GlowClubTransaction.objects.create(
            account=account,
            points=-reward.points_required,
            reason=f"Resgate: {reward.title}",
            redemption=redemption,
        )
        return redemption

    @classmethod
    def available_discount(cls, user, code: str, subtotal: Decimal) -> Decimal:
        if not code:
            return Decimal("0.00")
        from store.models import GlowClubRedemption
        redemption = (
            GlowClubRedemption.objects
            .select_related("reward")
            .filter(user=user, code__iexact=code.strip(), status="available", reward__reward_type="discount")
            .first()
        )
        if not redemption:
            return Decimal("0.00")
        discount = redemption.reward.discount_value or Decimal("0.00")
        return min(discount, subtotal).quantize(Decimal("0.01"))

    @classmethod
    def use_discount_code(cls, user, code: str):
        if not code:
            return None
        from store.models import GlowClubRedemption
        redemption = GlowClubRedemption.objects.filter(
            user=user,
            code__iexact=code.strip(),
            status="available",
            reward__reward_type="discount",
        ).first()
        if redemption:
            redemption.status = "used"
            redemption.used_at = timezone.now()
            redemption.save(update_fields=["status", "used_at"])
        return redemption
