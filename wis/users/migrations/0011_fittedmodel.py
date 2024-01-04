# Generated by Django 4.2.7 on 2024-01-03 22:43

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):
    dependencies = [
        ("filer", "0017_image__transparent"),
        ("users", "0010_delete_fittedmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="FittedModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "fitted_model",
                    filer.fields.file.FilerFileField(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="filer.file"
                    ),
                ),
            ],
        ),
    ]
