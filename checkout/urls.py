from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path(
        "checkout_succes/<order_number>",
        views.checkout_succes,
        name="checkout_succes",
    ),
    path(
        "cache_checkout_data/",
        views.cache_checkout_data,
        name="cache_checkout_data",
    ),
    path("wh/", webhook, name="webhook"),
    path('', views.checkout, name="checkout"),
]

