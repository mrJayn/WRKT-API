# Generated by Django 4.2.2 on 2023-09-25 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0026_remove_programexercise_week"),
    ]

    operations = [
        migrations.AddField(
            model_name="programexercise",
            name="week",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="api_users.programweek",
            ),
            preserve_default=False,
        ),
    ]
