from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.views.generic import View
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import Context, RequestContext
from .models import Product, Category, ProductDetail, Impression, UserProfile, Cart, CartItem, Order, OrderItem,ClassSettings
import json
from django.template.loader import render_to_string
from django.template import loader

from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm
from django.http import HttpResponse
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')


class AdminOnlyUser(View):
    def get(self, request):
        if request.user.is_staff:
            emails = UserProfile.objects.all().values_list('user__email',flat=True)
            z=''
            for email in emails:
                z=z+''+email+';'
            return HttpResponse(z)

# Create your views here.
class ContactUs(View):
    def post(self,request):
        params = {}
        params["class_settings"] = ClassSettings.objects.get(id=1)

        form = ContactForm(request.POST)
        if request.is_ajax():
            if form.is_valid():
                name = form.cleaned_data['first_name'] + form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                message = form.cleaned_data['message']

                try:
                    email_subject = 'Thank you for contacting us!'
                    email_body = loader.render_to_string('emails/contact.html',
                    {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'email': form.cleaned_data['email'],
                        'phone': form.cleaned_data['phone_number'],
                        'message': message,
                    })
                    Message = EmailMessage(email_subject, email_body, from_email='MBASQL <hello@mbasql.com>',to=[email], bcc=['hello@mbasql.com'],reply_to=['hello@mbasql.com'])
                    Message.content_subtype = "html"
                    Message.send()
                    params  = {'success': True, 'message': 'Thanks, we have received your message and will be in touch shortly!' }
                except:
                    params  = {'success': False, 'msg': 'Sorry! Something went wrong. Please try again. ' }
            else:
                params = {'success': False, 'msg': 'Sorry! Something went wrong. Please try again. Form not valid. ' }

            mimetype = 'application/json'
            return HttpResponse(json.dumps(params), mimetype)

# Create your views here.
class RegisterUser(View):
    def post(self, request):
        params = {}
        params["class_settings"] = ClassSettings.objects.get(id=1)

        form = RegistrationForm(request.POST)
        if form.is_valid():

            username=form.cleaned_data['username']
            existing_username = User.objects.filter(username=username).exists()
            if existing_username:
                params['registration_form'] =  form
                params['form'] = AuthenticationForm
                params['errors'] = "Username already taken."
                return render(request, 'registration/login.html',params)
            if not existing_username:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password'],
                    email = form.cleaned_data['email'],
                    is_active = True
                )
                user.userprofile.save();
                logout(request)
                user = authenticate(username=user.username, password=form.cleaned_data['password'])
                login(self.request, user)
                return redirect('shop browse')
            else:
                params['registration_form'] =  form
                params['form'] = AuthenticationForm
                params['errors']  = "We had trouble creating your account. Please check your info."
                return render(request, 'registration/login.html',params)
        else:
            params['registration_form'] =  form
            params['form'] = AuthenticationForm
            params['errors']  = "We had trouble creating your account. Please check your info."
            return render(request, 'registration/login.html',params)

    def get(self,request):
        return redirect('login')

class ViewCart(View):
    def get(self,request):
        user = request.user
        try:
            customer = UserProfile.objects.get(user=user)
        except:
            customer = None
        try:
            cart = Cart.objects.get(customer = customer)
        except:
            cart = None
        try:
            cart_items = CartItem.objects.filter(cart=cart)
        except:
            cart_items =  None
        total_value = 0
        for item in cart_items:
            total_value = total_value+(item.product.price * item.quantity)

        params = {}
        params["class_settings"] = ClassSettings.objects.get(id=1)

        params['total_value'] = total_value
        params['cart'] = cart
        params['cart_items'] = cart_items
        params["page"] = "shop"

        return render(request,'cart.html',params)
    def post(self,request):
        if 'buy' in request.POST:
            user = request.user
            try:
                customer = UserProfile.objects.get(user=user)
            except:
                customer = None
            try:
                cart = Cart.objects.get(customer = customer)
            except:
                cart = None
            try:
                cart_items = CartItem.objects.filter(cart=cart)
            except:
                cart_items =  None
            try:
                order = Order.objects.create(customer=customer)
                order.save()
            except:
                order = None
            for item in cart_items:
                try:
                    quantity = item.quantity
                    order = order
                    product = item.product
                    order_item = OrderItem.objects.create(product=product,quantity=quantity,order=order)
                    order_item.save()
                    item.delete()
                except:
                    pass
            order = order
            order_items = OrderItem.objects.filter(order=order)
            params = {}
            params['order'] = order
            params["page"] = "shop"
            params["class_settings"] = ClassSettings.objects.get(id=1)

            params['order_items'] = order_items

            return render(request,'thank_you.html',params)
        if 'update' in request.POST:
            user = request.user
            try:
                customer = UserProfile.objects.get(user=user)
            except:
                customer = None
            try:
                cart = Cart.objects.get(customer = customer)
            except:
                cart = None
            try:
                cart_items = CartItem.objects.filter(cart=cart)
            except:
                cart_items =  None
            for item in cart_items:
                try:
                    quantity = request.POST.getlist('products['+str(item.id)+']')
                    item.quantity = quantity[0]
                    item.save()
                    if quantity[0] == '0':
                        item.delete()
                except:
                    pass
            return redirect('cart')

class AddProductToCart(View):
    def post(self,request,id):
        if request.is_ajax():
            user = request.user
            try:
                customer = UserProfile.objects.get(user=user)
            except:
                customer = None
            if customer:
                try:
                    product = Product.objects.get(id=id)
                except:
                    product = None
                if product:
                    try:
                        cart = Cart.objects.get(customer = customer)
                    except:
                        cart = Cart.objects.create(customer=customer)
                        cart.save()
                    try:
                        cart_item = CartItem.objects.get(cart=cart,product=product)
                        cart_item.quantity = cart_item.quantity+1
                        cart_item.save()
                    except:
                        cart_item =  CartItem.objects.create(cart=cart,product=product,quantity=1)
                        cart_item.save()
                    try:
                        items_in_cart = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))
                    except:
                        items_in_cart = 0
                    params = {'success':True,'items':items_in_cart['quantity__sum']}
                    mimetype = 'application/json'
                    return HttpResponse(json.dumps(params), mimetype)


class Feedback(View):
    def get(self,request):
        params = {}
        params["class_settings"] = ClassSettings.objects.get(id=1)
        return render(request,'feedback.html',params)


class LandingPage(View):
    def get(self,request):
        params = {}
        params['contact_form'] =   ContactForm()
        params["class_settings"] = ClassSettings.objects.get(id=1)

        params['form'] = AuthenticationForm
        if request.user.is_authenticated():
            return render(request,'landing_logged_in.html',params)
        else:
            return render(request,'landing.html',params)

class ProductDetailPage(View):
    def get(self,request,id):

        product = Product.objects.get(id=id)
        product_details = ProductDetail.objects.filter(product = product)

        params = {}
        params["product"] = product
        params["product_details"] = product_details
        params["page"] = "shop"
        params["class_settings"] = ClassSettings.objects.get(id=1)

        requestor = None
        if request.user.is_authenticated():
            try:
                requestor = UserProfile.objects.get(user=request.user.id)
            except:
                requestor = UserProfile.objects.create(user=request.user)
                requestor.save()

        impression_instance = Impression(product=product, user=requestor)
        impression_instance.save()
        return render(request,'product_detail_page.html',params)

class ShopBrowse(View):
    def get(self,request):

        categories = Category.objects.all()
        category_dict = []
        for category in categories:
            product = Product.objects.filter(category=category).order_by('?').first()
            category_dict.append((category,product))

        params = {}
        params["page"] = "shop"

        params["categories"] = categories
        params["categories_products"] = category_dict
        params["class_settings"] = ClassSettings.objects.get(id=1)

        return render(request,'shop_browse.html',params)


class ViewSlides(View):
    def get(self,request):
        params = {}
        params["page"] = "lessons"
        params["class_settings"] = ClassSettings.objects.get(id=1)

        return render(request,'slides/table_of_contents.html',params)

class ViewSlideLesson(View):
    def get(self,request,lesson):
        params = {}

        params["page"] = "lessons"
        params["class_settings"] = ClassSettings.objects.get(id=1)

        return render(request,'slides/'+lesson+'.html',params)

class CategoryBrowse(View):
    def get(self,request,slug):
        category = Category.objects.get(slug=slug)
        params = {}
        params["current_category"] = category
        params["page"] = "shop"
        params["class_settings"] = ClassSettings.objects.get(id=1)

        params["products"] = Product.objects.filter(category=category)
        return render(request,'category_browse.html',params)
