"""Aichatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Aichatbot import views as admins_views
from paitent import views as paitent_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admins_views.index, name='index'),
    path('home/', admins_views.home, name='home'),
    path('about/', admins_views.admins, name='admins'),
    path('adminloginaction/', admins_views.adminloginaction, name='adminloginaction'),

    path('adminshome/',admins_views.adminshome, name='adminshome'),
    path('adminpaitent/',admins_views.adminpaitent, name='adminpaitent'),
    path('adminslogout/',admins_views.adminslogout, name='adminslogout'),
    path('AdminActiveUsers/',admins_views.AdminActiveUsers, name='AdminActiveUsers'),

    path('paitent/', paitent_views.paitent, name='paitent'),
    path('userregisterAction/',paitent_views.userregisterAction, name='userregisterAction'),
    path('userhome/',paitent_views.userhome, name='userhome'),
    path('userloginaction/', paitent_views.userloginaction, name='userloginaction'),
    path('userlogout/', paitent_views.userlogout, name='userlogout'),

    path('connectchatbot/', paitent_views.connectchatbot, name='connectchatbot'),
    path('get', paitent_views.get_bot_response, name='get_bot_response'),

    path('userdisease/', paitent_views.userdisease, name='userdisease'),
    path('userdiseasepredictionaction/', paitent_views.userdiseasepredictionaction, name='userdiseasepredictionaction'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)