# Generated by Django 4.2.9 on 2024-11-24 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0016_time_alter_range_m_options_remove_item_program_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="time",
            name="end",
            field=models.DateTimeField(null=True, verbose_name="время конца"),
        ),
        migrations.AlterField(
            model_name="time",
            name="start",
            field=models.DateTimeField(null=True, verbose_name="время начала"),
        ),
    ]