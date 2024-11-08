# Generated by Django 4.2.2 on 2023-12-06 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0094_remove_defaultlibraryexercise_profile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="libraryexercise",
            name="equipment",
            field=models.CharField(
                choices=[
                    ("BARBELL", "Barbell"),
                    ("DUMBELL", "Dumbell"),
                    ("SMITH_MACHINE", "Smith Machine"),
                    ("MACHINE", "Machine"),
                    ("CABLE", "Cable"),
                    ("EZ_BAR", "Ez Bar"),
                    ("BODY_WEIGHT", "Body-Weight"),
                    ("FREE_WEIGHT", "Free-Weight"),
                    ("BANDED", "Banded"),
                    ("", "none"),
                ],
                default="",
                max_length=13,
            ),
        ),
    ]
