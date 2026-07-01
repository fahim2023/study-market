from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    """
    A broad academic subject (e.g. Biology, Law, Computer Science).
    Courses are grouped under a Subject so the browse page can filter
    by subject before narrowing down to a specific course.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    """
    A specific course within a Subject (e.g. "A-Level Biology",
    "Introduction to Law"). Documents are categorised under a Course,
    which is what buyers actually filter and browse by.
    """

    LEVEL_CHOICES = [
        ("gcse", "GCSE"),
        ("a_level", "A-Level"),
        ("undergraduate", "Undergraduate"),
        ("postgraduate", "Postgraduate"),
        ("other", "Other"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    name = models.CharField(max_length=150)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    exam_board = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    class Meta:
        ordering = ["subject__name", "name"]
        unique_together = ("subject", "name", "level")

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.subject.name}-{self.name}-{self.level}")
        super().save(*args, **kwargs)
