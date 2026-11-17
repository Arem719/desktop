from .cart import Cart
from .models import Category


def shop(request):
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(request.user.favorites.values_list("product_id", flat=True))
    return {
        "nav_categories": Category.objects.all(),
        "cart_count": len(Cart(request)),
        "fav_ids": fav_ids,
        "free_delivery_from": 1000,
    }
