from django.contrib import admin
from .models import Subscription

# Register your models here.


@admin.register(Subscription)
class SubscribedUser(admin.ModelAdmin):
    list_display = ("email", "created_on")