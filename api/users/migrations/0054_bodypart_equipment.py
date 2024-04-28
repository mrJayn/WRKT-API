# Generated by Django 4.2.2 on 2023-10-16 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0053_orderedexa_programweek_alter_orderedexa_day"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bodypart",
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
                ("name", models.CharField(max_length=10)),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="Equipment",
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
                ("name", models.CharField(max_length=10)),
            ],
            options={"ordering": ["name"],},
        ),
    ]
