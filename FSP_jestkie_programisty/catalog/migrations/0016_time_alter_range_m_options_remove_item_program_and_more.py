# Generated by Django 4.2.9 on 2024-11-24 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0015_alter_item_served_alter_mass_mass_end_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Time",
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
                    "name",
                    models.CharField(
                        help_text="Имя объекта", max_length=150, verbose_name="название"
                    ),
                ),
                (
                    "canonical_name",
                    models.CharField(
                        default="default",
                        help_text="Каноническое название элемента",
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="каноническое имя",
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="время начала"
                    ),
                ),
                (
                    "end",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="время конца"
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.AlterModelOptions(
            name="range_m",
            options={"verbose_name": "Маштаб", "verbose_name_plural": "Маштабы"},
        ),
        migrations.RemoveField(
            model_name="item",
            name="program",
        ),
        migrations.DeleteModel(
            name="Program",
        ),
        migrations.AlterField(
            model_name="item",
            name="time",
            field=models.ForeignKey(
                help_text="Выберите Время",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="catalog_ешьу",
                to="catalog.time",
                verbose_name="Время",
            ),
        ),
    ]
