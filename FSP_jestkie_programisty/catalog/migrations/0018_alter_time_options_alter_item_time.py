# Generated by Django 4.2.9 on 2024-11-24 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0017_alter_time_end_alter_time_start"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="time",
            options={"verbose_name": "время", "verbose_name_plural": "времена"},
        ),
        migrations.AlterField(
            model_name="item",
            name="time",
            field=models.ForeignKey(
                help_text="Выберите Время",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="catalog_time",
                to="catalog.time",
                verbose_name="Время",
            ),
        ),
    ]
