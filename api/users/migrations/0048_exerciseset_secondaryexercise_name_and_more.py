# Generated by Django 4.2.2 on 2023-10-10 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0047_secondaryexercise_set"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExerciseSet",
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
                ("sets", models.CharField(blank=True, default="", max_length=50)),
                ("reps", models.CharField(blank=True, default="", max_length=50)),
                ("weight", models.CharField(blank=True, default="", max_length=50)),
                ("percent", models.FloatField(blank=True, null=True)),
            ],
            options={"ordering": ["order"],},
        ),
        migrations.AddField(
            model_name="secondaryexercise",
            name="name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
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
            name="workout_day",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exs",
                to="api_users.day",
            ),
        ),
        migrations.DeleteModel(name="Set",),
        migrations.AddField(
            model_name="exerciseset",
            name="exercise",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sets",
                to="api_users.exercise",
            ),
        ),
    ]
