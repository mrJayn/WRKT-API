# Generated by Django 4.2.2 on 2023-09-25 20:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0021_alter_programweek_options_remove_programweek_order"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="programexercise", options={"ordering": ["week"]},
        ),
        migrations.RemoveField(model_name="programexercise", name="program_week",),
        migrations.AddField(
            model_name="programexercise",
            name="day",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1),
                ],
            ),
        ),
        migrations.AddField(
            model_name="programexercise",
            name="program",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="api_users.program",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="programexercise",
            name="week",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="accessoryexercise",
            name="primary_ex",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accessories",
                to="api_users.programexercise",
            ),
        ),
        migrations.DeleteModel(name="ProgramWeek",),
    ]
