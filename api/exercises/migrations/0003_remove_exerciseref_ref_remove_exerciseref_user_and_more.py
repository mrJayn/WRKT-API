# Generated by Django 4.2.2 on 2024-08-22 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_exercises", "0002_remove_baseexercise_is_enabled_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="exerciseref", name="ref",),
        migrations.RemoveField(model_name="exerciseref", name="user",),
        migrations.DeleteModel(name="Exercise",),
        migrations.DeleteModel(name="ExerciseRef",),
    ]