from django.utils import timezone

from .models import UserProfile,Cart,CartItem
from django.db.models import Sum


def in_cart_context(request):
    context_data = dict()
    try:
        items_in_cart = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))
    except:
        items_in_cart = 0
    context_data['items_in_cart'] = items_in_cart
    return context_data