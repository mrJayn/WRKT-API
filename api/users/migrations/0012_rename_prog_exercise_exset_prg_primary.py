# Generated by Django 4.2.2 on 2023-09-25 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0011_programprimaryexercise_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exset", old_name="prog_exercise", new_name="prg_primary",
        ),
    ]
