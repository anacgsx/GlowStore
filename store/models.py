from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=180, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BeautyStore(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    slogan = models.CharField(max_length=160)
    description = models.TextField()
    logo = models.ImageField(upload_to='stores/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='stores/banners/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(BeautyStore, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    color_name = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_trending = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=20)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.store.name}-{self.name}')
        super().save(*args, **kwargs)

    @property
    def has_discount(self):
        return self.old_price and self.old_price > self.price

    @property
    def discount_percent(self):
        if not self.has_discount:
            return 0
        return round((1 - self.price / self.old_price) * 100)

    def __str__(self):
        return self.name


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Produto favorito'
        verbose_name_plural = 'Produtos favoritos'


class FavoriteStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(BeautyStore, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'store')
        verbose_name = 'Loja favorita'
        verbose_name_plural = 'Lojas favoritas'


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Criado'),
        ('paid', 'Pago'),
        ('preparing', 'Preparando'),
        ('sent', 'Enviado'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    payment_method = models.CharField(max_length=30)
    shipping_method = models.CharField(max_length=30)
    reward_code = models.CharField(max_length=30, blank=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    shipping_total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    discount_total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    glow_points_earned = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def total(self):
        return self.unit_price * self.quantity


class GlowClubAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='glowclub')
    points = models.PositiveIntegerField(default=0)
    lifetime_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conta GlowClub'
        verbose_name_plural = 'Contas GlowClub'

    @property
    def tier(self):
        if self.lifetime_points >= 1000:
            return 'Ruby'
        if self.lifetime_points >= 500:
            return 'Rose'
        return 'Glow'

    def __str__(self):
        return f'GlowClub de {self.user.username}'


class GlowReward(models.Model):
    DISCOUNT = 'discount'
    PRODUCT = 'product'
    REWARD_TYPES = [
        (DISCOUNT, 'Desconto'),
        (PRODUCT, 'Produto'),
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=220)
    points_required = models.PositiveIntegerField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES, default=DISCOUNT)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Recompensa GlowClub'
        verbose_name_plural = 'Recompensas GlowClub'
        ordering = ['points_required']

    def __str__(self):
        return self.title


class GlowClubRedemption(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('used', 'Usado'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='glowclub_redemptions')
    reward = models.ForeignKey(GlowReward, on_delete=models.PROTECT)
    code = models.CharField(max_length=30, unique=True)
    points_spent = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Resgate GlowClub'
        verbose_name_plural = 'Resgates GlowClub'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reward.title} - {self.user.username}'


class GlowClubTransaction(models.Model):
    account = models.ForeignKey(GlowClubAccount, on_delete=models.CASCADE, related_name='transactions')
    points = models.IntegerField()
    reason = models.CharField(max_length=180)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    redemption = models.ForeignKey(GlowClubRedemption, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transação GlowClub'
        verbose_name_plural = 'Transações GlowClub'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.points} pontos - {self.reason}'
