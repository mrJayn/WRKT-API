# Generated by Django 4.2.2 on 2023-11-20 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0079_alter_workout_options_workout_modified_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workout", options={"ordering": ["-active", "order"]},
        ),
        migrations.RemoveField(model_name="workout", name="modified_date",),
    ]
