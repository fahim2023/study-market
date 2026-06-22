from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Subject, Course


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "level", "exam_board")
    list_filter = ("subject", "level")
    search_fields = ("name", "subject__name")
    prepopulated_fields = {"slug": ("name",)}
