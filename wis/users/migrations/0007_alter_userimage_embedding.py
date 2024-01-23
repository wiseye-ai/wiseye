# Generated by Django 4.2.7 on 2024-01-03 21:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_remove_user_image_userimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userimage",
            name="embedding",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=list, size=None),
        ),
    ]