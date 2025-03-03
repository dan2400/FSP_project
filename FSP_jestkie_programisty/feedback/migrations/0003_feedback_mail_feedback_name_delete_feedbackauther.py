# Generated by Django 4.2.9 on 2024-11-20 17:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_remove_feedback_canonical_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='mail',
            field=models.EmailField(
                default=django.utils.timezone.now,
                max_length=254,
                verbose_name='электронная почта',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(
                default=django.utils.timezone.now,
                max_length=150,
                verbose_name='имя',
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='FeedbackAuther',
        ),
    ]
