# Generated by Django 4.2.2 on 2024-02-25 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0106_alter_customuser_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="inactive_start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
