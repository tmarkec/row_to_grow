from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('shipping_return/', views.shipping, name='shipping'),
    path('privacy_policy/', views.privacy, name='privacy'),
    path('', views.index, name='home'),
]
