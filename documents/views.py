from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Document
from courses.models import Subject
from payments.models import Purchase
from reviews.models import Review
from .forms import DocumentForm
from django.contrib import messages


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

    reviews = Review.objects.filter(document=document).select_related("reviewer")

    user_has_reviewed = (
        request.user.is_authenticated
        and Review.objects.filter(reviewer=request.user, document=document).exists()
    )

    context = {
        "document": document,
        "has_purchased": has_purchased,
        "reviews": reviews,
        "user_has_reviewed": user_has_reviewed,
    }
    return render(request, "documents/detail.html", context)


@login_required
def seller_dashboard(request):
    """
    Seller dashboard — shows all documents uploaded by the logged-in user.
    """
    documents = Document.objects.filter(seller=request.user).order_by("-created_at")

    return render(
        request,
        "documents/seller_dashboard.html",
        {
            "documents": documents,
        },
    )


@login_required
def upload_document(request):
    """
    Allows sellers to upload a new document.
    """
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.seller = request.user
            document.save()
            messages.success(request, "Your document has been uploaded successfully.")
            return redirect("documents:seller_dashboard")
    else:
        form = DocumentForm()

    return render(
        request,
        "documents/upload.html",
        {
            "form": form,
        },
    )


@login_required
def edit_document(request, slug):
    """
    Allows sellers to edit their own documents.
    """
    document = get_object_or_404(Document, slug=slug, seller=request.user)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Your document has been updated.")
            return redirect("documents:seller_dashboard")
    else:
        form = DocumentForm(instance=document)

    return render(
        request,
        "documents/edit_document.html",
        {
            "form": form,
            "document": document,
        },
    )
