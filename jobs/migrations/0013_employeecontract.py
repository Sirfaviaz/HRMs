# Generated by Django 5.1.1 on 2024-10-19 15:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0012_delete_employeecontract"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployeeContract",
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
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "workshift",
                    models.CharField(
                        choices=[
                            ("Day", "Day Shift"),
                            ("Night", "Night Shift"),
                            ("Rotating", "Rotating Shift"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "worktype",
                    models.CharField(
                        choices=[
                            ("Full-Time", "Full-Time"),
                            ("Part-Time", "Part-Time"),
                            ("Contract", "Contract"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "employee_type",
                    models.CharField(
                        choices=[
                            ("Permanent", "Permanent"),
                            ("Temporary", "Temporary"),
                            ("Intern", "Intern"),
                        ],
                        max_length=50,
                    ),
                ),
                ("contract_start_date", models.DateField()),
                ("contract_end_date", models.DateField(blank=True, null=True)),
                ("accepted", models.BooleanField(default=False)),
                ("date_accepted", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "candidate_application",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contract",
                        to="jobs.candidateapplication",
                    ),
                ),
            ],
        ),
    ]
