# Generated by Django 4.2.2 on 2023-11-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0074_rename_programweek_week"),
    ]

    operations = [
        migrations.AlterField(
            model_name="program",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="program",
            name="startdate",
            field=models.DateField(blank=True, default="2023-11-11", null=True),
        ),
    ]
