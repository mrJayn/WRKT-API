# Generated by Django 4.2.2 on 2024-02-21 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0099_alter_customuser_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="inactive_start_date",
            field=models.DateTimeField(
                blank=True,
                help_text="Datetime of when the field `is_active` was set False. No value while the field `is_active` is True.",
                null=True,
                verbose_name="inactive start date",
            ),
        ),
    ]
