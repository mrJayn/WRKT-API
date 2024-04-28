# Generated by Django 4.2.2 on 2023-11-03 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0067_alter_profile_day_one_wkday"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exercise", options={"ordering": ["day", "week", "order"]},
        ),
        migrations.RenameField(
            model_name="exercise", old_name="workout_day", new_name="day",
        ),
        migrations.RenameField(
            model_name="exercise", old_name="program_week", new_name="week",
        ),
        migrations.AlterField(
            model_name="exercise",
            name="name",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="exerciseset",
            name="exercise",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sets",
                to="api_users.exercise",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="secondaryexercise",
            name="exercise",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="secondary",
                to="api_users.exercise",
            ),
            preserve_default=False,
        ),
    ]
