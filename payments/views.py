import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from documents.models import Document
from .models import Purchase

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    already_purchased = Purchase.objects.filter(
        buyer=request.user, document=document
    ).exists()
    if already_purchased:
        return redirect("documents:detail", slug=document.slug)

    if request.method == "POST":
        intent = stripe.PaymentIntent.create(
            amount=int(document.price * 100),
            currency="gbp",
            metadata={"document_id": document.id, "user_id": request.user.id},
        )
        return JsonResponse({"client_secret": intent.client_secret})

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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == "payment_intent.succeeded":
        intent = event.data.object
        document_id = intent.metadata.get("document_id")
        user_id = intent.metadata.get("user_id")

        if document_id and user_id:
            try:
                document = Document.objects.get(id=document_id)
                from django.contrib.auth.models import User

                user = User.objects.get(id=user_id)
                Purchase.objects.get_or_create(
                    buyer=user,
                    document=document,
                    defaults={
                        "stripe_payment_intent": intent.id,
                        "amount_paid": document.price,
                    },
                )
            except (Document.DoesNotExist, User.DoesNotExist):
                return HttpResponse(status=400)

    return HttpResponse(status=200)
