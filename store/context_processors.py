from .patterns import CartSession


def cart_counter(request):
    return {'cart_count': CartSession(request).count() if hasattr(request, 'session') else 0}
