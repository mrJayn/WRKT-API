# Generated by Django 4.2.2 on 2024-08-20 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0137_alter_libraryexercise_profile_alter_profile_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="libraryexercise", old_name="custom", new_name="is_custom",
        ),
    ]