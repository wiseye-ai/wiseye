# Generated by Django 4.2.7 on 2024-01-03 20:40

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ("users", "0005_user_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="image",
        ),
        migrations.CreateModel(
            name="UserImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                (
                    "embedding",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(), blank=True, null=True, size=None
                    ),
                ),
                (
                    "image",
                    filer.fields.image.FilerImageField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_image",
                        to=settings.FILER_IMAGE_MODEL,
                        verbose_name="image",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "user image",
                "verbose_name_plural": "user images",
            },
        ),
    ]
