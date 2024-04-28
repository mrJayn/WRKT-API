# Generated by Django 4.2.2 on 2023-09-25 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0029_programexercise_week"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exset", options={"ordering": ["order", "id"]},
        ),
        migrations.AlterModelOptions(
            name="programexercise", options={"ordering": ["week", "day"]},
        ),
        migrations.RenameField(
            model_name="accessoryexercise",
            old_name="primary_ex",
            new_name="program_ex",
        ),
        migrations.RenameField(
            model_name="exset", old_name="accessory_exercise", new_name="accessory_ex",
        ),
    ]
