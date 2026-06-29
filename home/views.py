from django.shortcuts import render
from django.db.models import Avg
from documents.models import Document
from courses.models import Subject


def home(request):
    featured_documents = (
        Document.objects.filter(status="published")
        .select_related("course", "course__subject", "seller")
        .annotate(avg_rating=Avg("reviews__rating"))
        .order_by("-created_at")[:6]
    )

    subjects = Subject.objects.all()

    purchased_ids = []
    if request.user.is_authenticated:
        from payments.models import Purchase

        purchased_ids = list(
            Purchase.objects.filter(buyer=request.user).values_list(
                "document_id", flat=True
            )
        )

    context = {
        "featured_documents": featured_documents,
        "subjects": subjects,
        "purchased_ids": purchased_ids,
    }
    return render(request, "home/index.html", context)
