# Generated by Django 4.2.2 on 2023-09-26 20:24

import utils.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_users", "0033_rename_accessoryexercise_programaccessory_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exset",
            name="percent",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="program",
            name="duration",
            field=utils.fields.models.IntegerField(
                default=4,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="programweek",
            name="week",
            field=models.IntegerField(default=0),
        ),
    ]
