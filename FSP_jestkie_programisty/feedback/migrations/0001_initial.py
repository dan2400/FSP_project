# Generated by Django 4.2.9 on 2024-11-08 16:36

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True, verbose_name='опубликовано'
                    ),
                ),
                (
                    'canonical_name',
                    models.CharField(
                        default='default',
                        help_text='Каноническое название элемента',
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name='каноническое имя',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Имя объекта',
                        max_length=150,
                        verbose_name='Имя',
                    ),
                ),
                (
                    'text',
                    django_ckeditor_5.fields.CKEditor5Field(
                        help_text='Место для сообщения',
                        verbose_name='описание',
                    ),
                ),
                (
                    'created_on',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='время создания'
                    ),
                ),
                (
                    'mail',
                    models.EmailField(
                        help_text='почта клиента',
                        max_length=254,
                        verbose_name='почта',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
