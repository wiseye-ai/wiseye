import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField

from wis.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Wiseye.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    image = FilerImageField(
        verbose_name=_("image"),
        null=True,
        blank=True,
        related_name="user_image",
        on_delete=models.SET_NULL,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
