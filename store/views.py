from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CheckoutForm, RegisterForm
from .models import BeautyStore, Category, FavoriteProduct, FavoriteStore, Order, Product
from .patterns import (
    AddToCartCommand,
    CartSession,
    CheckoutFacade,
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
    return render(request, 'store/cart.html', {'items': cart_service.items(), 'subtotal': cart_service.subtotal()})


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
        request.POST.get('shipping_method', 'standard')
    )
    return render(request, 'store/checkout.html', {'form': form, 'preview': preview, 'items': facade.cart.items()})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def profile(request):
    orders = request.user.orders.order_by('-created_at')
    return render(request, 'store/profile.html', {'orders': orders})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})
