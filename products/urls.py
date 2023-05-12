from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
    path('add_review/<product_id>', views.add_review, name='add_review'),
    path('delete_review/<int:review_id>', views.del_review, name='del_review'),
    path('update_review/<int:review_id>',
         views.update_review, name='update_review'),
    path('', views.all_products, name='products'),
]
