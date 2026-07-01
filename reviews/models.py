from django.contrib.auth.models import User
from django.db import models

from documents.models import Document


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("document", "reviewer")

    def __str__(self):
        return (
            f"{self.reviewer.username} — "
            f"{self.document.title} ({self.rating}★)"
        )
