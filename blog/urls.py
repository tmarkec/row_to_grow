from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('<slug:slug>/', views.BlogDetail.as_view(), name='blog_detail'),
    path('like/<slug:slug>/', views.BlogLikes.as_view(), name="blog_like"),
    path('', views.BlogList.as_view(), name='blog'),
]
