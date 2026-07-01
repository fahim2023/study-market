from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile


class ProfileSignalTest(TestCase):
    """
    Tests that a Profile is automatically created whenever a new User
    is registered, via the post_save signal in signals.py.
    """

    def test_profile_created_automatically_on_user_creation(self):
        user = User.objects.create_user(
            username="testbuyer", password="testpass123")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_new_profile_defaults_to_not_a_seller(self):
        user = User.objects.create_user(
            username="testbuyer2", password="testpass123")
        self.assertFalse(user.profile.is_seller)
