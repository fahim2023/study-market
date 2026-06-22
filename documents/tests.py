from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase

from courses.models import Course, Subject
from .models import Document, DocumentTag


class DocumentTagModelTest(TestCase):
    """
    Tests for the DocumentTag model.
    """

    def test_tag_str_returns_name(self):
        tag = DocumentTag.objects.create(name="Exam Prep")
        self.assertEqual(str(tag), "Exam Prep")


class DocumentModelTest(TestCase):
    """
    Tests for the Document model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testseller", password="testpass123"
        )
        self.subject = Subject.objects.create(name="Biology")
        self.course = Course.objects.create(
            subject=self.subject,
            name="A-Level Biology",
            level="a_level",
        )

    def test_document_slug_auto_generated(self):
        document = Document.objects.create(
            seller=self.user,
            course=self.course,
            title="Cell Biology Notes",
            description="Detailed notes on cell biology.",
            preview_text="A preview of cell biology notes.",
            price="4.99",
        )
        self.assertEqual(document.slug, "cell-biology-notes")
