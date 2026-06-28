from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("browse/", views.browse, name="browse"),
    path("document/<slug:slug>/", views.document_detail, name="detail"),
    path("seller/dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/upload/", views.upload_document, name="upload"),
    path("seller/edit/<slug:slug>/", views.edit_document, name="edit"),
    path("seller/delete/<slug:slug>/", views.delete_document, name="delete"),
]
