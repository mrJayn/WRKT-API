# Generated by Django 4.2.2 on 2023-10-07 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0045_alter_program_options_remove_program_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exercise",
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
                ("order", models.IntegerField(default=0)),
                ("name", models.CharField(blank=True, default="", max_length=50)),
                (
                    "program_week",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gen_ex",
                        to="api_users.programweek",
                    ),
                ),
                (
                    "workout_day",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gen_ex",
                        to="api_users.day",
                    ),
                ),
            ],
            options={"ordering": ["workout_day", "program_week", "order"],},
        ),
    ]
