# Generated by Django 4.2.2 on 2023-09-23 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "api_users",
            "0007_alter_exercise_program_week_alter_exercise_workout_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgramWeekExercise",
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
                (
                    "program_week",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises",
                        to="api_users.programweek",
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(name="exset", options={"ordering": ["order"]},),
        migrations.AlterModelOptions(
            name="libraryexercise", options={"ordering": ["custom", "id"]},
        ),
        migrations.RemoveField(model_name="exset", name="exercise",),
        migrations.AddField(
            model_name="exset",
            name="wrkt_exercise",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sets",
                to="api_users.workoutexercise",
            ),
        ),
        migrations.DeleteModel(name="Exercise",),
        migrations.AddField(
            model_name="exset",
            name="prog_exercise",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sets",
                to="api_users.programweekexercise",
            ),
        ),
    ]