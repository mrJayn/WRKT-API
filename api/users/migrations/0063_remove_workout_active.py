# Generated by Django 4.2.2 on 2023-10-23 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0062_alter_workout_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="workout", name="active",),
    ]
