from django.urls import path
from . import views

urlpatterns = [
    path('success/', views.contact_success, name='contact_success'),
    path('', views.contact, name='contact'),
]
