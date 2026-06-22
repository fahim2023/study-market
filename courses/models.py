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
