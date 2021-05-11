from django.contrib import admin
from .models import (UserProfile,Order,Category, Product, ProductAttribute, ProductDetail,Impression, Cart, CartItem, OrderItem,ClassSettings)

admin.site.register((UserProfile,Order,Category, Product, ProductAttribute, ProductDetail,Impression,Cart, CartItem,OrderItem,ClassSettings))