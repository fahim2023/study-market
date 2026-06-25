from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from documents.models import Document
from payments.models import Purchase
from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Only buyers who have purchased the document can review it
    has_purchased = Purchase.objects.filter(
        buyer=request.user, document=document
    ).exists()
    if not has_purchased:
        messages.error(
            request, "You must purchase this document before leaving a review."
        )
        return redirect("documents:detail", slug=document.slug)

    # Prevent duplicate reviews
    already_reviewed = Review.objects.filter(
        reviewer=request.user, document=document
    ).exists()
    if already_reviewed:
        messages.error(request, "You have already reviewed this document.")
        return redirect("documents:detail", slug=document.slug)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.document = document
            review.reviewer = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect("documents:detail", slug=document.slug)
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "document": document,
        },
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    document = review.document

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect("documents:detail", slug=document.slug)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/edit_review.html",
        {
            "form": form,
            "document": document,
            "review": review,
        },
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    document = review.document

    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect("documents:detail", slug=document.slug)

    return render(
        request,
        "reviews/delete_review.html",
        {
            "review": review,
            "document": document,
        },
    )
