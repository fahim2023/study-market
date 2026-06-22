from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from courses.models import Course


class DocumentTag(models.Model):
    """
    A short label that can be applied to many documents
    (e.g. "Exam Prep", "Summary Notes", "Past Paper").
    Many-to-many with Document.
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Document(models.Model):
    """
    The core model — a study document listed for sale by a seller.
    Full content is gated behind payment; preview_text is visible
    to everyone so buyers can evaluate before purchasing.
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    preview_text = models.TextField(
        blank=True,
        help_text="A short teaser visible to all users before purchase.",
    )
    file = models.FileField(upload_to="documents/")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )
    tags = models.ManyToManyField(DocumentTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
