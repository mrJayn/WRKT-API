# Generated by Django 4.2.2 on 2024-08-15 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0132_alter_workout_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile", options={"verbose_name_plural": "Profile"},
        ),
    ]
