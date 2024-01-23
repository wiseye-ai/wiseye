# Generated by Django 4.2.7 on 2024-01-17 22:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0012_userlogs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userimage",
            name="embedding",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.FloatField(), blank=True, null=True, size=None
            ),
        ),
    ]