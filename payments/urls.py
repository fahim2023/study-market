from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/<int:document_id>/", views.checkout, name="checkout"),
    path("success/<int:document_id>/", views.payment_success, name="success"),
    path("cancel/<int:document_id>/", views.payment_cancel, name="cancel"),
    path("webhook/", views.stripe_webhook, name="stripe-webhook"),
    path("my-purchases/", views.my_purchases, name="my_purchases"),
]
