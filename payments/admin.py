from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("buyer", "document", "amount_paid", "created_at")
    list_filter = ("created_at",)
    search_fields = ("buyer__username", "document__title")
