# Generated by Django 4.2.7 on 2023-11-22 20:45

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ("users", "0004_alter_user_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=filer.fields.image.FilerImageField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_image",
                to=settings.FILER_IMAGE_MODEL,
                verbose_name="image",
            ),
        ),
    ]