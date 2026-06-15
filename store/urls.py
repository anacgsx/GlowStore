from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lojas/', views.stores_page, name='stores'),
    path('categorias/', views.categories_page, name='categories'),
    path('buscar/', views.search, name='search'),
    path('loja/<slug:slug>/', views.store_detail, name='store_detail'),
    path('produto/<slug:slug>/', views.product_detail, name='product_detail'),
    path('favoritos/', views.favorites, name='favorites'),
    path('favoritar-produto/<int:product_id>/', views.toggle_favorite_product, name='toggle_favorite_product'),
    path('favoritar-loja/<int:store_id>/', views.toggle_favorite_store, name='toggle_favorite_store'),
    path('carrinho/', views.cart, name='cart'),
    path('carrinho/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrinho/remover/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('pedido/<int:order_id>/', views.order_detail, name='order_detail'),
    path('perfil/', views.profile, name='profile'),
    path('glowclub/resgatar/<int:reward_id>/', views.redeem_reward, name='redeem_reward'),
    path('cadastro/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
