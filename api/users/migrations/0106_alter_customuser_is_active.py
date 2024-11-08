# Generated by Django 4.2.2 on 2024-02-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0105_remove_customuser_inactive_start_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
