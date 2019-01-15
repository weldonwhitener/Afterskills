from django.db import models
from django.utils.timezone import now as now
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.template.defaultfilters import slugify

class Animal(models.Model):
    species = models.CharField(max_length=256,blank=True,null=True,default=None)
    breed = models.CharField(max_length=256,blank=True,null=True,default=None)
    age = models.PositiveIntegerField()
    name =  models.CharField(max_length=256,blank=True,null=True,default=None)


class ClassSettings(models.Model):
    feedback_link = models.CharField(max_length=256,blank=True,null=True,default=None)
    slack_link = models.CharField(max_length=256,blank=True,null=True,default=None)
    udemy_link = models.CharField(max_length=256,blank=True,null=True,default=None)
    udemy_discount_link = models.CharField(max_length=256,blank=True,null=True,default=None)
    show_slides_today = models.BooleanField(default=False)
    show_slack_link = models.BooleanField(default=False)
    show_feedback_link = models.BooleanField(default=False)
    show_udemy_link = models.BooleanField(default=False)
    show_udemy_discount_link = models.BooleanField(default=False)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=256,blank=True,null=True,default=None)
    address = models.CharField(max_length=256,blank=True,null=True,default=None)
    show_slides = models.BooleanField(default=False)
    slug       = models.SlugField(max_length=100, unique=True)
    created     = models.DateTimeField(editable=False,default=now,blank=True,null=True)
    modified    = models.DateTimeField(default=now,blank=True,null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = now()
            proposed = slugify(self.user.first_name+"  "+self.user.last_name)
            slugcrement = 0
            while(UserProfile.objects.filter(slug=proposed).exists()):
                slugcrement +=1
                proposed = proposed + "-" + str(slugcrement)
            self.slug = proposed
        self.modified = now()
        return super(UserProfile, self).save(*args, **kwargs)

def generate_product_image(self, filename):
    url = "products/product-%s-%s" % (self.name, filename)
    return url

class Order(models.Model):
    customer =  models.ForeignKey('UserProfile')
    created     = models.DateTimeField(editable=False,default=now,blank=True,null=True)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = now()
        return super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order =  models.ForeignKey('Order')
    product =  models.ForeignKey('Product')
    quantity = models.PositiveIntegerField()
    created     = models.DateTimeField(editable=False,default=now,blank=True,null=True)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = now()
        return super(OrderItem, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.order.customer) + '' + str(self.product.name)

class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    category =  models.ForeignKey('Category', blank=True, default=None)
    photo = models.ImageField(upload_to=generate_product_image,blank=True)
    manufacturer = models.CharField(max_length=300,blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=300, default="€")
    bullet_point_a = models.CharField(max_length=300,blank=True,default=None)
    bullet_point_b = models.CharField(max_length=300,blank=True,default=None)
    bullet_point_c = models.CharField(max_length=300,blank=True,default=None)
    bullet_point_d = models.CharField(max_length=300,blank=True,default=None)
    bullet_point_e = models.CharField(max_length=300,blank=True,default=None)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer =  models.ForeignKey('UserProfile')
    created     = models.DateTimeField(editable=False,default=now,blank=True,null=True)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = now()
        return super(Cart, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.customer)


class CartItem(models.Model):
    cart =  models.ForeignKey('Cart')
    product =  models.ForeignKey('Product')
    quantity = models.PositiveIntegerField()
    created     = models.DateTimeField(editable=False,default=now,blank=True,null=True)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = now()
        return super(CartItem, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.cart.customer) + '' + str(self.product.name)

class Impression(models.Model):
    product =  models.ForeignKey('Product')
    user =  models.ForeignKey('UserProfile', blank=True, null=True, default=None)
    created     = models.DateTimeField(editable=False,default=now,blank=True,null=True)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = now()
        return super(Impression, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

class ProductDetail(models.Model):
 product = models.ForeignKey('Product', related_name='details')
 attribute = models.ForeignKey('ProductAttribute')
 value = models.CharField(max_length=500)
 description = models.TextField(blank=True)

 def __str__(self):
    return u'%s: %s - %s' % (self.product, self.attribute, self.value)

class ProductAttribute(models.Model):
 name = models.CharField(max_length=300)
 measure = models.CharField(max_length=300, blank=True, default=None)
 description = models.TextField(blank=True)

 def __str__(self):
    return u'%s' % self.name


def get_user_profile(slug):
    return UserProfile.objects.get(slug=slug)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)