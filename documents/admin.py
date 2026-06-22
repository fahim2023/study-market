from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Document, DocumentTag


@admin.register(DocumentTag)
class DocumentTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "course", "price", "status", "created_at")
    list_filter = ("status", "course__subject", "course")
    search_fields = ("title", "seller__username")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
