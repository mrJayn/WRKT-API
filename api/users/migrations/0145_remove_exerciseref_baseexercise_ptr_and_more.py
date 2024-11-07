# Generated by Django 4.2.2 on 2024-08-23 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0144_delete_baseexerciseref"),
    ]

    operations = [
        migrations.RemoveField(model_name="exerciseref", name="baseexercise_ptr",),
        migrations.RemoveField(model_name="exerciseref", name="user",),
        migrations.RemoveField(model_name="exerciseset", name="exercise",),
        migrations.DeleteModel(name="Exercise",),
        migrations.DeleteModel(name="ExerciseRef",),
        migrations.DeleteModel(name="ExerciseSet",),
    ]