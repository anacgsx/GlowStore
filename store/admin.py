from django.contrib import admin
from .models import BeautyStore, Category, FavoriteProduct, FavoriteStore, Order, OrderItem, Product

admin.site.register(Category)
admin.site.register(BeautyStore)
admin.site.register(Product)
admin.site.register(FavoriteProduct)
admin.site.register(FavoriteStore)
admin.site.register(OrderItem)
admin.site.register(Order)
