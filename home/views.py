from django.shortcuts import render
from documents.models import Document
from courses.models import Subject


def home(request):
    """
    Landing page view. Shows hero, subject grid,
    featured documents and how it works section.
    """
    featured_documents = (
        Document.objects.filter(status="published")
        .select_related("course", "course__subject", "seller")
        .order_by("-created_at")[:6]
    )

    subjects = Subject.objects.all()

    context = {
        "featured_documents": featured_documents,
        "subjects": subjects,
    }
    return render(request, "home/index.html", context)
