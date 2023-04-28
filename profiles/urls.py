from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('info/', views.info, name='info'),
    path('history/', views.history, name='history'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
]