# Generated by Django 4.2.2 on 2024-02-25 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0104_alter_customuser_username"),
    ]

    operations = [
        migrations.RemoveField(model_name="customuser", name="inactive_start_date",),
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
