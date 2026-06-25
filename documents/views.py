from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Document
from courses.models import Subject
from payments.models import Purchase


def browse(request):
    """
    Main browse/homepage view. Lists all published documents,
    with optional filtering by subject and keyword search.
    """
    documents = Document.objects.filter(status="published").select_related(
        "course", "course__subject", "seller"
    )

    subjects = Subject.objects.all()

    subject_slug = request.GET.get("subject")
    if subject_slug:
        documents = documents.filter(course__subject__slug=subject_slug)

    query = request.GET.get("q")
    if query:
        documents = documents.filter(title__icontains=query)

    context = {
        "documents": documents,
        "subjects": subjects,
        "selected_subject": subject_slug,
        "query": query,
    }
    return render(request, "documents/browse.html", context)


def document_detail(request, slug):
    """
    Document detail page. Shows preview content to everyone.
    Full content is only shown if the user has purchased this document.
    The purchase check is the core gating mechanism of StudyMarket.
    """
    document = get_object_or_404(Document, slug=slug, status="published")

    has_purchased = (
        request.user.is_authenticated
        and Purchase.objects.filter(buyer=request.user, document=document).exists()
    )

    context = {
        "document": document,
        "has_purchased": has_purchased,
    }
    return render(request, "documents/detail.html", context)
