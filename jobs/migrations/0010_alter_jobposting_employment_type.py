# Generated by Django 5.1.1 on 2024-10-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0009_alter_jobposting_employment_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobposting",
            name="employment_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("full_time", "Full-Time"),
                    ("part_time", "Part-Time"),
                    ("contract", "Contract"),
                    ("internship", "Internship"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
