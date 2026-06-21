from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Extends Django's built-in User with StudyMarket-specific fields.

    Every registered user gets a Profile automatically. Only users who
    choose to sell documents need to fill in the seller fields
    (institution/bio) — is_seller flips to True once they complete the
    "Become a seller" form.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    is_seller = models.BooleanField(default=False)
    institution = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return self.user.username
