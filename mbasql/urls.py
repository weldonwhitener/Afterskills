"""mbasql URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import  include, url
from shop.views import RegisterUser
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required
from shop.forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test
from shop.views import AdminOnlyUser,Logout,LandingPage,Feedback,ViewSlides,ViewSlideLesson,ContactUs
from django.contrib.auth.views import password_reset, password_reset_done


login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/logout/')



urlpatterns = [
    url(r'^hadouken/', admin.site.urls),
    #url(r'^kookoowalla/$', login_required(AdminOnlyUser.as_view()), name='oo'),

    url(r'^$',  LandingPage.as_view(), name='register'),

    url(r'^explorer/', include('explorer.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^register/$', RegisterUser.as_view(), name='register'),
    url(r'^login/$', login_forbidden(django.contrib.auth.views.login),{'extra_context': {'registration_form':RegistrationForm}}, name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),

    url(r'^login/password/reset/$', password_reset, {'template_name': 'registration/password_reset.html'},name="password_reset"),
    url(r'^login/password/reset/sent/$', password_reset_done,{'template_name': 'registration/password_reset_sent.html'},name='password_reset_done'),
    url(r'^login/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', django.contrib.auth.views.password_reset_confirm,{'template_name': 'registration/password_reset_confirm.html'},name="password_reset_confirm"),
    url(r'^login/password/reset/done/$', django.contrib.auth.views.password_reset_complete, {'template_name': 'registration/password_reset_done.html'}, name="password_reset_complete"),

    url(r'^feedback/$', login_required(Feedback.as_view()), name='feedback'),
    url(r'^lessons/$', login_required(ViewSlides.as_view()), name='view slides'),
    url(r'^slides/(?P<lesson>[\w-]+)/$', login_required(ViewSlideLesson.as_view()), name='view lesson slides'),
    url(r'^contact/$', (ContactUs.as_view()), name='contact'),



]
