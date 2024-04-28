# Generated by Django 4.2.2 on 2023-11-11 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0072_alter_program_duration_alter_program_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="program",
            name="startdate",
            field=models.DateField(default=datetime.date.today, verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="programweek",
            name="week_id",
            field=models.PositiveIntegerField(),
        ),
    ]