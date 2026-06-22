from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Document
from courses.models import Subject

# Create your views here.


def browse(request):
    """
    Main browse/homepage view. Lists all published documents,
    with optional filtering by subject and keyword search.
    """
    documents = Document.objects.filter(status="published").select_related(
        "course", "course__subject", "seller"
    )

    subjects = Subject.objects.all()

    # Filter by subject if selected
    subject_slug = request.GET.get("subject")
    if subject_slug:
        documents = documents.filter(course__subject__slug=subject_slug)

    # Search by title keyword
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

    # TODO: wire up real purchase check once payments app exists.
    # has_purchased will always be False until Purchase model is built.
    has_purchased = False

    context = {
        "document": document,
        "has_purchased": has_purchased,
    }
    return render(request, "documents/detail.html", context)
