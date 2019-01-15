from django.utils import timezone

from .models import UserProfile,Cart,CartItem,Category,ClassSettings
from django.db.models import Sum

def in_cart_context(request):
    context_data = dict()
    items_in_cart = 0
    try:
        cart = Cart.objects.get(customer=request.user.userprofile)
        items_in_cart = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))
        items_in_cart = items_in_cart['quantity__sum']
    except:
        items_in_cart = 0
    if not items_in_cart:
        items_in_cart = 0
    context_data['items_in_cart'] = items_in_cart
    context_data["categories"] = Category.objects.all()

    return context_data



def class_settings_context(request):
    context_data = dict()
    context_data["class_settings"] = ClassSettings.objects.get(id=1)


    return context_data