# Generated by Django 4.2.2 on 2023-09-23 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "api_users",
            "0006_alter_exercise_options_alter_libraryexercise_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercise",
            name="program_week",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exs",
                to="api_users.programweek",
            ),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="workout",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exs",
                to="api_users.workout",
            ),
        ),
        migrations.AlterField(
            model_name="workoutexercise",
            name="name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]
