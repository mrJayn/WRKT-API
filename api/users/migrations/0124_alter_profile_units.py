# Generated by Django 4.2.2 on 2024-05-01 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0123_alter_profile_preferred_theme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="units",
            field=models.CharField(
                choices=[("lbs", "lbs"), ("kgs", "kgs")], default="lbs", max_length=3
            ),
        ),
    ]