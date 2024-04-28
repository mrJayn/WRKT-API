# Generated by Django 4.2.2 on 2023-09-25 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0024_programweek"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="programexercise", options={"ordering": ["day"]},
        ),
        migrations.RemoveField(model_name="programexercise", name="program",),
        migrations.AlterField(
            model_name="programexercise",
            name="week",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="api_users.programweek",
            ),
        ),
    ]
