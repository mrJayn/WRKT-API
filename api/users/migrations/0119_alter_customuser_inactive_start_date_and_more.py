# Generated by Django 4.2.2 on 2024-03-02 20:03

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0118_alter_program_startdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="inactive_start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                error_messages={"unique": "This phone number is already being used."},
                max_length=128,
                null=True,
                region=None,
                unique=True,
            ),
        ),
    ]
