# Generated by Django 4.2.2 on 2023-09-26 21:54

import utils.fields
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api_users", "0035_alter_programweek_options_remove_programweek_week"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programexercise",
            name="day",
            field=utils.fields.RangeIntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(2),
                ],
            ),
        ),
    ]
