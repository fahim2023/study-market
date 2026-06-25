from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from documents.models import Document
from courses.models import Course, Subject
from payments.models import Purchase
from .models import Review


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testreviewer", password="testpass123"
        )
        self.subject = Subject.objects.create(name="Mathematics")
        self.course = Course.objects.create(
            name="A-Level Maths",
            subject=self.subject,
            level="a_level",
        )
        self.document = Document.objects.create(
            title="Test Notes",
            seller=self.user,
            course=self.course,
            price=9.99,
            status="published",
        )

    def test_review_str(self):
        review = Review.objects.create(
            reviewer=self.user,
            document=self.document,
            rating=5,
            comment="Excellent notes.",
        )
        self.assertEqual(str(review), "testreviewer — Test Notes (5★)")

    def test_unpurchased_user_cannot_review(self):
        self.client.login(username="testreviewer", password="testpass123")
        response = self.client.post(
            reverse("reviews:add_review", args=[self.document.id]),
            {"rating": 5, "comment": "Great notes."},
        )
        self.assertEqual(Review.objects.count(), 0)
        self.assertRedirects(
            response, reverse("documents:detail", args=[self.document.slug])
        )

    def test_purchased_user_can_review(self):
        Purchase.objects.create(
            buyer=self.user,
            document=self.document,
            stripe_payment_intent="pi_test_123",
            amount_paid=9.99,
        )
        self.client.login(username="testreviewer", password="testpass123")
        response = self.client.post(
            reverse("reviews:add_review", args=[self.document.id]),
            {"rating": 4, "comment": "Really helpful notes."},
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().rating, 4)
