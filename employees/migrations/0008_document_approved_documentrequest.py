# Generated by Django 5.1.1 on 2024-10-14 09:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0007_alter_employee_position_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="approved",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="DocumentRequest",
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
                ("document_name", models.CharField(max_length=255)),
                ("message", models.TextField(blank=True, null=True)),
                (
                    "requested_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("completed", "Completed")],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_requests",
                        to="employees.employee",
                    ),
                ),
                (
                    "requested_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="requests_made",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
