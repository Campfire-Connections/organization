# Generated by Django 5.0.6 on 2024-09-28 12:00

import django.contrib.auth.mixins
import django.views.generic.edit
import pages.mixins.forms
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0003_organization_last_activity_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeleteView",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django.contrib.auth.mixins.LoginRequiredMixin,
                django.contrib.auth.mixins.PermissionRequiredMixin,
                models.Model,
                pages.mixins.forms.SuccessMessageMixin,
                django.views.generic.edit.DeleteView,
            ),
        ),
        migrations.DeleteModel(
            name="OrganizationSettings",
        ),
    ]
