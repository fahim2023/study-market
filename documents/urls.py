from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.browse, name="browse"),
    path("document/<slug:slug>/", views.document_detail, name="detail"),
]
