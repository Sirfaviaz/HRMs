# Generated by Django 5.1.1 on 2024-10-07 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("departments", "0003_historicaldepartment_position_historicalposition"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobPosting",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=255)),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("Full-Time", "Full-Time"),
                            ("Part-Time", "Part-Time"),
                            ("Contract", "Contract"),
                            ("Internship", "Internship"),
                        ],
                        max_length=50,
                    ),
                ),
                ("posted_date", models.DateField(auto_now_add=True)),
                ("closing_date", models.DateField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "department",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="departments.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CandidateApplication",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("resume", models.FileField(upload_to="resumes/")),
                ("cover_letter", models.TextField(blank=True, null=True)),
                ("application_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Applied", "Applied"),
                            ("Reviewed", "Reviewed"),
                            ("Interview Scheduled", "Interview Scheduled"),
                            ("Offered", "Offered"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Applied",
                        max_length=50,
                    ),
                ),
                (
                    "job_posting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="jobs.jobposting",
                    ),
                ),
            ],
        ),
    ]
