# Generated by Django 4.2.2 on 2023-09-25 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0025_alter_programexercise_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="programexercise", name="week",),
    ]
