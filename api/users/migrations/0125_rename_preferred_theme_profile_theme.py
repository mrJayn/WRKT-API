# Generated by Django 4.2.2 on 2024-05-02 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0124_alter_profile_units"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="preferred_theme", new_name="theme",
        ),
    ]
