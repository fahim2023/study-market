import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from documents.models import Document
from .models import Purchase

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Prevent buying something you already own
    already_purchased = Purchase.objects.filter(
        buyer=request.user, document=document
    ).exists()
    if already_purchased:
        return redirect("documents:detail", slug=document.slug)

    if request.method == "POST":
        intent = stripe.PaymentIntent.create(
            amount=int(document.price * 100),  # Stripe uses pence/cents
            currency="gbp",
            metadata={"document_id": document.id, "user_id": request.user.id},
        )
        return render(
            request,
            "payments/checkout.html",
            {
                "document": document,
                "client_secret": intent.client_secret,
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            },
        )

    return render(
        request,
        "payments/checkout.html",
        {
            "document": document,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        },
    )


@login_required
def payment_success(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    payment_intent_id = request.GET.get("payment_intent")

    if payment_intent_id:
        Purchase.objects.get_or_create(
            buyer=request.user,
            document=document,
            defaults={
                "stripe_payment_intent": payment_intent_id,
                "amount_paid": document.price,
            },
        )

    return render(request, "payments/success.html", {"document": document})


@login_required
def payment_cancel(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, "payments/cancel.html", {"document": document})
