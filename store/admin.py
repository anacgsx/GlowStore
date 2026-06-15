from django.contrib import admin
from .models import (
    BeautyStore,
    Category,
    FavoriteProduct,
    FavoriteStore,
    GlowClubAccount,
    GlowClubRedemption,
    GlowClubTransaction,
    GlowReward,
    Order,
    OrderItem,
    Product,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BeautyStore)
class BeautyStoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slogan', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_featured',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'category', 'price', 'stock', 'is_trending')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('store', 'category', 'is_trending')
    search_fields = ('name', 'description', 'store__name')


admin.site.register(FavoriteProduct)
admin.site.register(FavoriteStore)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(GlowClubAccount)
admin.site.register(GlowReward)
admin.site.register(GlowClubRedemption)
admin.site.register(GlowClubTransaction)
