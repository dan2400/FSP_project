import uuid

import django.db.models
import django.utils.timezone
import django_ckeditor_5.fields


class Feedback(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        NEW = 'new', 'New'
        WIP = 'wip', 'Work is progress'
        ANSWERED = 'ans', 'Answered'

    name = django.db.models.CharField('имя', max_length=150)
    mail = django.db.models.EmailField('электронная почта')

    text = django_ckeditor_5.fields.CKEditor5Field(
        'описание',
        help_text=('Место для сообщения'),
    )
    created_on = django.db.models.DateTimeField(
        'время создания',
        auto_now_add=True,
        unique=False,
        null=False,
    )
    status = django.db.models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.NEW,
    )


class FeedbackFile(django.db.models.Model):
    def get_path(self, filename):
        return f'uploads/{self.feedback_id}/{uuid.uuid4()}_{filename}'

    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name='files',
        on_delete=django.db.models.CASCADE,
    )

    file = django.db.models.FileField(
        'файл',
        upload_to=get_path,
        blank=True,
    )


__all__ = [
    'Feedback',
]
