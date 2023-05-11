from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class UserContact(admin.ModelAdmin):
    list_display = ("fname", "lname", "email", "subject", "message")
    search_fields = ['email']
