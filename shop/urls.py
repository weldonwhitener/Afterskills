from django.conf.urls import url
from .views import ProductDetailPage,CategoryBrowse,ShopBrowse,AddProductToCart,ViewCart,RegisterUser
from django.contrib.auth.decorators import login_required

urlpatterns = [
   url(r'^product/(?P<id>[\w-]+)/add/$', login_required(AddProductToCart.as_view()), name='product add to cart'),
   url(r'^product/(?P<id>[\w-]+)/$', login_required(ProductDetailPage.as_view()), name='product detail page'),
   url(r'^category/(?P<slug>[\w-]+)/$', login_required(CategoryBrowse.as_view()), name='category browse'),
   url(r'^cart/$', login_required(ViewCart.as_view()), name='cart'),

   url(r'^$', login_required(ShopBrowse.as_view()), name='shop browse'),

]
