# Generated by Django 4.2.2 on 2023-11-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0078_alter_libraryexercise_bodypart_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workout", options={"ordering": ["modified_date", "order"]},
        ),
        migrations.AddField(
            model_name="workout",
            name="modified_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
