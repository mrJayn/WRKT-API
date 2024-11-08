# Generated by Django 4.2.2 on 2024-01-09 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0095_alter_libraryexercise_equipment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="notifs", new_name="notifications",
        ),
        migrations.RemoveField(model_name="profile", name="basic_editor",),
        migrations.RemoveField(model_name="profile", name="prefers_metric",),
        migrations.RemoveField(model_name="profile", name="time_offset",),
        migrations.AddField(
            model_name="profile",
            name="units",
            field=models.CharField(
                choices=[("LBS", "lbs"), ("KGS", "kgs")], default="LBS", max_length=3
            ),
        ),
        migrations.AlterField(
            model_name="libraryexercise",
            name="custom",
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
