from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Document
from courses.models import Subject
from payments.models import Purchase
from reviews.models import Review
from .forms import DocumentForm
from django.contrib import messages


def browse(request):
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

    sort = request.GET.get("sort", "newest")
    if sort == "price_asc":
        documents = documents.order_by("price")
    elif sort == "price_desc":
        documents = documents.order_by("-price")
    elif sort == "a_z":
        documents = documents.order_by("title")
    elif sort == "z_a":
        documents = documents.order_by("-title")
    elif sort == "top_rated":
        from django.db.models import Avg

        documents = documents.annotate(avg_rating=Avg("reviews__rating")).order_by(
            "-avg_rating"
        )
    else:
        documents = documents.order_by("-created_at")

    paginator = Paginator(documents, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "documents": page_obj,
        "subjects": subjects,
        "selected_subject": subject_slug,
        "query": query,
        "page_obj": page_obj,
        "sort": sort,
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
    document = get_object_or_404(Document, slug=slug, seller=request.user)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            doc = form.save(commit=False)
            if not request.FILES.get("file"):
                doc.file = document.file
            doc.save()
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


@login_required
def delete_document(request, slug):
    """
    Allows sellers to delete their own documents.
    """
    document = get_object_or_404(Document, slug=slug, seller=request.user)

    if request.method == "POST":
        document.delete()
        messages.success(request, "Your document has been deleted.")
        return redirect("documents:seller_dashboard")

    return render(
        request,
        "documents/delete_document.html",
        {
            "document": document,
        },
    )
