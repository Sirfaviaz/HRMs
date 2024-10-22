# Generated by Django 5.1.1 on 2024-10-15 08:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0003_stage_jobposting_filled_jobposting_vacancies_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StageSet",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="jobposting",
            name="stage_set",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="jobs.stageset",
            ),
        ),
        migrations.AddField(
            model_name="stage",
            name="stage_set",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stages",
                to="jobs.stageset",
            ),
        ),
    ]
