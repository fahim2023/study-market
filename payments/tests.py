from django.test import TestCase

from django.contrib.auth.models import User
from documents.models import Document
from courses.models import Course, Subject
from .models import Purchase

# Create your tests here.


class PurchaseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testbuyer", password="testpass123"
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

    def test_purchase_str(self):
        purchase = Purchase.objects.create(
            buyer=self.user,
            document=self.document,
            stripe_payment_intent="pi_test_12345",
            amount_paid=9.99,
        )
        self.assertEqual(str(purchase), "testbuyer → Test Notes")

    def test_duplicate_purchase_prevented(self):
        Purchase.objects.create(
            buyer=self.user,
            document=self.document,
            stripe_payment_intent="pi_test_123",
            amount_paid=9.99,
        )

        with self.assertRaises(Exception):
            Purchase.objects.create(
                buyer=self.user,
                document=self.document,
                stripe_payment_intent="pi_test_456",
                amount_paid=9.99,
            )

    def test_checkout_requires_login(self):
        self.client.logout()
        response = self.client.get(f"/payments/checkout/{self.document.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])
