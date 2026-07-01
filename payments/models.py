from django.db import models

from django.contrib.auth.models import User

from documents.models import Document

# Create your models here.


class Purchase(models.Model):
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases")
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="purchases"
    )
    stripe_payment_intent = models.CharField(max_length=200, unique=True)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("buyer", "document")

    def __str__(self):
        return f"{self.buyer.username} → {self.document.title}"
