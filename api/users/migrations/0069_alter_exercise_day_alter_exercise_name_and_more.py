# Generated by Django 4.2.2 on 2023-11-03 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0068_alter_exercise_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercise",
            name="day",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="api_users.day",
            ),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="order",
            field=models.PositiveIntegerField(db_index=True, verbose_name="order"),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="week",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="api_users.programweek",
            ),
        ),
    ]
