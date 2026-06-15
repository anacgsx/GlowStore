from .models import FavoriteProduct, FavoriteStore
from .patterns import CartSession


def cart_counter(request):
    return {'cart_count': CartSession(request).count() if hasattr(request, 'session') else 0}


def favorite_ids(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {'favorite_product_ids': set(), 'favorite_store_ids': set()}
    return {
        'favorite_product_ids': set(FavoriteProduct.objects.filter(user=request.user).values_list('product_id', flat=True)),
        'favorite_store_ids': set(FavoriteStore.objects.filter(user=request.user).values_list('store_id', flat=True)),
    }
