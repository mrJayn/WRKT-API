# Generated by Django 4.2.2 on 2023-09-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0008_programweekexercise_alter_exset_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exset",
            name="percent",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="exset",
            name="reps",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="exset",
            name="set",
            field=models.CharField(blank=True, default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name="exset",
            name="weight",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]
