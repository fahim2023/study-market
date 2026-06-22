from django.shortcuts import render
from .models import Document
from courses.models import Subject

# Create your views here.


def browse(request):
    """
    Main browse/homepage view. Lists all published documents,
    with optional filtering by subject.
    """
    documents = Document.objects.filter(status="published").select_related(
        "course", "course__subject", "seller"
    )

    subjects = Subject.objects.all()

    # Filter by subject if selected
    subject_slug = request.GET.get("subject")
    if subject_slug:
        documents = documents.filter(course__subject__slug=subject_slug)

    context = {
        "documents": documents,
        "subjects": subjects,
        "selected_subject": subject_slug,
    }
    return render(request, "documents/browse.html", context)
