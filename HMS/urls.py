"""HMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from pages.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login'),
    path('home', home_view, name='home'),
    path('create/', room_create, name='room-create'),
    path('billing/', bill_view, name='billing'),
    path('booking/', book_view, name='booking'),
    path('', include('django.contrib.auth.urls')),
    path('room/<str:my_pk>', room_detail, name='room-detail'),
    path('resturant/', resturant_bill, name='resturant'),
    path('resturant/<int:my_order>/', resturant_reciept, name='resturant-reciept'),
    path('Gym/', gym_bill, name='gym'),
    path('Gym/<int:my_usage_id>/', gym_reciept, name='gym-reciept'),
    path('Pool/', pool_bill, name='pool'),
    path('Pool/<int:my_usage_id>/', pool_reciept, name='pool-reciept'),
    path('billing/<int:my_phone>/', checkout_bill, name='bill-final'),
]
