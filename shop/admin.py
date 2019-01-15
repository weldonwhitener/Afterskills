from django.contrib import admin
from .models import (Animal, UserProfile,Order,Category, Product, ProductAttribute, ProductDetail,Impression, Cart, CartItem, OrderItem,ClassSettings)

admin.site.register((Animal, UserProfile,Order,Category, Product, ProductAttribute, ProductDetail,Impression,Cart, CartItem,OrderItem,ClassSettings))