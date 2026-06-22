from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Subject, Course


class SubjectModelTest(TestCase):
    """
    Tests for the Subject model.
    """

    def setUp(self):
        self.subject = Subject.objects.create(name="Mathematics")

    def test_subject_slug_auto_generated(self):
        self.assertEqual(self.subject.slug, "mathematics")

    def test_course_slug_auto_generated(self):
        course = Course.objects.create(
            subject=self.subject,
            name="A-Level Mathematics",
            level="a_level",
        )
        self.assertEqual(course.slug, "mathematics-a-level-mathematics-a_level")
