from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from servico_GlowClub import GlowClubService
from .forms import CheckoutForm, RegisterForm
from .models import BeautyStore, Category, FavoriteProduct, FavoriteStore, GlowReward, Order, Product
from .patterns import (
    AddToCartCommand,
    CartSession,
    CheckoutFacade,
    PaymentStrategyFactory,
    ShippingStrategyFactory,
    ToggleFavoriteProductCommand,
    ToggleFavoriteStoreCommand,
)


def home(request):
    categories = Category.objects.all()
    stores = BeautyStore.objects.all()
    products = Product.objects.select_related('store', 'category').filter(is_trending=True)[:8]
    return render(request, 'store/home.html', {
        'categories': categories,
        'stores': stores,
        'products': products,
    })


def stores_page(request):
    stores = BeautyStore.objects.prefetch_related('products').all()
    return render(request, 'store/stores.html', {'stores': stores})


def categories_page(request):
    categories = Category.objects.prefetch_related('products').all()
    active = request.GET.get('categoria')
    products = Product.objects.select_related('store', 'category').all()
    if active:
        products = products.filter(category__slug=active)
    return render(request, 'store/categories.html', {
        'categories': categories,
        'products': products,
        'active': active,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.select_related('store', 'category').none()
    stores = BeautyStore.objects.none()
    categories = Category.objects.none()
    if query:
        products = Product.objects.select_related('store', 'category').filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(store__name__icontains=query) |
            Q(category__name__icontains=query)
        )
        stores = BeautyStore.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        categories = Category.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/search.html', {
        'query': query,
        'products': products,
        'stores': stores,
        'categories': categories,
    })


def store_detail(request, slug):
    beauty_store = get_object_or_404(BeautyStore, slug=slug)
    products = beauty_store.products.select_related('category').all()
    categories = Category.objects.filter(products__store=beauty_store).distinct()
    active = request.GET.get('categoria')
    if active:
        products = products.filter(category__slug=active)
    return render(request, 'store/store_detail.html', {
        'beauty_store': beauty_store,
        'products': products,
        'categories': categories,
        'active': active,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('store', 'category'), slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})


@login_required
def favorites(request):
    product_favorites = FavoriteProduct.objects.filter(user=request.user).select_related('product', 'product__store')
    store_favorites = FavoriteStore.objects.filter(user=request.user).select_related('store')
    return render(request, 'store/favorites.html', {
        'product_favorites': product_favorites,
        'store_favorites': store_favorites,
    })


@login_required
def toggle_favorite_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ToggleFavoriteProductCommand(request.user, product).execute()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_favorite_store(request, store_id):
    beauty_store = get_object_or_404(BeautyStore, id=store_id)
    ToggleFavoriteStoreCommand(request.user, beauty_store).execute()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    AddToCartCommand(request, product, quantity).execute()
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def remove_from_cart(request, product_id):
    CartSession(request).remove(product_id)
    return redirect('cart')


def cart(request):
    cart_service = CartSession(request)
    return render(request, 'store/cart.html', {
        'items': cart_service.items(),
        'subtotal': cart_service.subtotal(),
    })


@login_required
def checkout(request):
    facade = CheckoutFacade(request)
    if not facade.cart.items():
        return redirect('cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = facade.finish_order(**form.cleaned_data)
            return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm(initial={'full_name': request.user.get_full_name() or request.user.username})
    preview = facade.preview(
        request.POST.get('payment_method', 'credit'),
        request.POST.get('shipping_method', 'standard'),
        request.POST.get('reward_code', ''),
    )
    return render(request, 'store/checkout.html', {
        'form': form,
        'preview': preview,
        'items': facade.cart.items(),
        'checkout_config': facade.frontend_config(),
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def profile(request):
    orders = request.user.orders.order_by('-created_at')
    account = GlowClubService.account_for(request.user)
    rewards = GlowReward.objects.filter(is_active=True).select_related('product')
    redemptions = request.user.glowclub_redemptions.select_related('reward')[:8]
    return render(request, 'store/profile.html', {
        'orders': orders,
        'account': account,
        'rewards': rewards,
        'redemptions': redemptions,
    })


@login_required
@require_POST
def redeem_reward(request, reward_id):
    reward = get_object_or_404(GlowReward, id=reward_id, is_active=True)
    try:
        redemption = GlowClubService.redeem(request.user, reward)
        messages.success(request, f'Resgate criado: {redemption.code}')
    except ValueError as error:
        messages.error(request, str(error))
    return redirect('profile')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            GlowClubService.account_for(user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})
