from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('info/', views.info, name='info'),
]