# Generated by Django 4.2.2 on 2023-10-05 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0044_alter_program_options_alter_workout_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(name="program", options={"ordering": ["order"]},),
        migrations.RemoveField(model_name="program", name="active",),
    ]
