# Generated by Django 4.2.2 on 2023-09-23 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0003_alter_libraryexercise_max"),
    ]

    operations = [
        migrations.AlterField(
            model_name="libraryexercise",
            name="bodypart",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="libraryexercise",
            name="equipment",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="libraryexercise",
            name="name",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
