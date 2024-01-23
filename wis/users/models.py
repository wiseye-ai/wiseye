import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from wis.users.helpers import detect_faces
from wis.users.managers import UserManager


class User(AbstractUser):
    """!
    Default custom user model for Wiseye.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})


class UserImage(models.Model):
    """!
    Model used for keeping user photos, and their embeddings.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    image = FilerImageField(
        verbose_name=_("image"),
        null=True,
        blank=True,
        related_name="user_image",
        on_delete=models.SET_NULL,
    )
    embedding = ArrayField(
        base_field=models.FloatField(),
        null=True,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("user image")
        verbose_name_plural = _("user images")

    def save(self, *args, **kwargs):
        """!
        Method used for saving the model to database and invoking the function used for creating
        an embedding for the photo.
        """
        super().save(*args, **kwargs)
        if self.image and not kwargs.get("update_fields"):
            self.embedding = detect_faces(self.image.file.path)
            self.save(update_fields=["embedding"])


class FittedModel(models.Model):
    fitted_model = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL)


class UserLogsType(models.TextChoices):
    """!
    Class used to keep the information about type of authentication process activity.
    """

    ## Indicates that user has been recognized by the system and the password is correct # noqa
    RECOGNIZED = "recognized", _("recognized")
    ## Indicates that user has been recognized by the system but the password is incorrect # noqa
    WRONG_PASSWORD = "wrong password", _("wrong password")
    ## Indicates that user has not been recognized by the system # noqa
    UNKNOWN = "unknown user", _("unknown user")


class UserLogs(models.Model):
    """!
    Model used for logging activity in the system. It keeps information about user, time of the activity and type
     (if the process was successful, if the user has been recognized).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=100, choices=UserLogsType.choices, null=True, blank=True)

    @staticmethod
    def create_logs(user: User = None, log_type: str = UserLogsType.UNKNOWN):
        """!
        Function used to create UserLogs instances.
        @params user Used to represent which user took a part in a authentication process, if no user has been
             recognized, it's null
        @param log_type Used to define what type of log should be created
        """
        if log_type == UserLogsType.RECOGNIZED:
            return UserLogs.objects.create(user=user, log_type=UserLogsType.RECOGNIZED)

        if log_type == UserLogsType.WRONG_PASSWORD:
            return UserLogs.objects.create(user=user, log_type=UserLogsType.WRONG_PASSWORD)

        if log_type == UserLogsType.UNKNOWN:
            return UserLogs.objects.create(user=user, log_type=UserLogsType.UNKNOWN)
