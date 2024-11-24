# Generated by Django 4.2.9 on 2024-11-07 20:00

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    replaces = [
        ('catalog', '0011_item_is_on_main_alter_item_text'),
        ('catalog', '0012_item_created_item_updated'),
        ('catalog', '0013_alter_item_created_alter_item_updated'),
    ]

    dependencies = [
        (
            'catalog',
            '0008_alter_item_options_alter_item_category_mainimage_and_more_squashed_0010_alter_item_text',
        ),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_on_main',
            field=models.BooleanField(
                default=False, verbose_name='На главной'
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(
                help_text='Описание должно содержать "превосходно" или "роскошно"',
                verbose_name='описание',
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='created',
            field=models.DateTimeField(
                auto_now_add=True, unique=False, null=True, verbose_name='время создания'
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='updated',
            field=models.DateTimeField(
                auto_now=True, unique=False, null=True, verbose_name='время изменения'
            ),
        ),
    ]
