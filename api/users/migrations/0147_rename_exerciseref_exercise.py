# Generated by Django 4.2.2 on 2024-08-23 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "api_exercises",
            "0003_remove_exerciseref_ref_remove_exerciseref_user_and_more",
        ),
        ("api_users", "0146_exerciseref"),
    ]

    operations = [
        migrations.RenameModel(old_name="ExerciseRef", new_name="Exercise",),
    ]
