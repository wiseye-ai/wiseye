# Generated by Django 4.2.7 on 2024-01-03 22:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_alter_fittedmodel_fitted_model"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FittedModel",
        ),
    ]
