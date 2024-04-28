# Generated by Django 4.2.2 on 2023-10-14 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0051_alter_program_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercise",
            name="order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="OrderedExA",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(db_index=True, verbose_name="order"),
                ),
                ("name", models.CharField(blank=True, default="", max_length=50)),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ord_exs",
                        to="api_users.day",
                    ),
                ),
            ],
            options={"ordering": ["order"], "abstract": False,},
        ),
    ]
