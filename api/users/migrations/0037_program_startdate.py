# Generated by Django 4.2.2 on 2023-09-26 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0036_alter_programexercise_day"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="startdate",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
    ]
