# Generated by Django 4.2.2 on 2023-12-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0092_alter_customlibraryexercise_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customlibraryexercise",
            name="bodypart",
            field=models.CharField(
                choices=[
                    ("CHEST", "Chest"),
                    ("BACK", "Back"),
                    ("ARMS", "Arms"),
                    ("SHOULDERS", "Shoulders"),
                    ("LEGS", "Legs"),
                    ("CORE", "Core"),
                    ("", "none"),
                ],
                default="",
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="customlibraryexercise",
            name="equipment",
            field=models.CharField(
                choices=[
                    ("BARBELL", "Barbell"),
                    ("DUMBELL", "Ez Bar"),
                    ("SMITH_MACHINE", "Dumbell"),
                    ("MACHINE", "Cable"),
                    ("CABLE", "Smith Machine"),
                    ("EX_BAR", "Machine"),
                    ("BODY_WEIGHT", "Body-Weight"),
                    ("FREE_WEIGHT", "Free-Weight"),
                    ("BANDED", "Banded"),
                    ("", "none"),
                ],
                default="",
                max_length=13,
            ),
        ),
        migrations.AlterField(
            model_name="defaultlibraryexercise",
            name="bodypart",
            field=models.CharField(
                choices=[
                    ("CHEST", "Chest"),
                    ("BACK", "Back"),
                    ("ARMS", "Arms"),
                    ("SHOULDERS", "Shoulders"),
                    ("LEGS", "Legs"),
                    ("CORE", "Core"),
                    ("", "none"),
                ],
                default="",
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="defaultlibraryexercise",
            name="equipment",
            field=models.CharField(
                choices=[
                    ("BARBELL", "Barbell"),
                    ("DUMBELL", "Ez Bar"),
                    ("SMITH_MACHINE", "Dumbell"),
                    ("MACHINE", "Cable"),
                    ("CABLE", "Smith Machine"),
                    ("EX_BAR", "Machine"),
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
