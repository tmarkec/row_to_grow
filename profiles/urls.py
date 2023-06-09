from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info, name='info'),
    path('history/', views.history, name='history'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/delete/<int:product_id>/',
         views.delete_from_wishlist, name='delete_from_wishlist'),
    path('accounts/password/change/',
         views.password_change, name='password_change'),
    path('order_history/<order_number>',
         views.order_history, name='order_history'),
    path('orders/<order_number>/pdf/',
         views.download_order_pdf, name='download_order_pdf'),
    path('', views.profile, name='profile'),
]
