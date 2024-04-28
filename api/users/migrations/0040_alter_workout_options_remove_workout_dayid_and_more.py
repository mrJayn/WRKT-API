# Generated by Django 4.2.2 on 2023-09-27 19:58

import api.users.models.workout
from django.db import migrations, models
import django.db.models.deletion
import utils.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api_users", "0039_alter_programaccessory_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workout",
            options={"ordering": ["name"]},
        ),
        migrations.RemoveField(
            model_name="workout",
            name="dayid",
        ),
        migrations.RemoveField(
            model_name="workout",
            name="groups",
        ),
        migrations.AlterField(
            model_name="workout",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wrkts",
                to="api_users.profile",
            ),
        ),
        migrations.RenameModel(
            old_name="WorkoutExercise",
            new_name="DayExercise",
        ),
        migrations.CreateModel(
            name="Day",
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
                ("dayid", utils.fields.RangeIntegerField(null=True)),
                ("name", models.CharField(default="", max_length=50)),
                (
                    "groups",
                    models.JSONField(default=dict),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workouts",
                        to="api_users.workout",
                    ),
                ),
            ],
            options={
                "ordering": ["dayid"],
            },
        ),
        migrations.AlterField(
            model_name="dayexercise",
            name="workout",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="api_users.day",
            ),
        ),
    ]