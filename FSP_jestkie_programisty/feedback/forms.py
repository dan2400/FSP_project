import django.forms

from feedback import models


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-cntrol'


class FeedbackForm(BootstrapForm):
    class Meta:
        model = models.Feedback
        exclude = (
            models.Feedback.id.field.name,
            models.Feedback.created_on.field.name,
            models.Feedback.status.field.name,
        )
        labels = {
            models.Feedback.name.field.name: 'Имя',
            models.Feedback.mail.field.name: ('Электронная почта',),
            models.Feedback.text.field.name: 'Сообщение',
        }
        help_text = {
            models.Feedback.name.field.name: 'Введите ваше имя',
            models.Feedback.mail.field.name: (
                'Введите ваш электронный адрес',
            ),
            models.Feedback.text.field.name: 'введите сообщение',
        }


class FeedbackFileForm(BootstrapForm):
    class Meta:
        model = models.FeedbackFile

        fields = (models.FeedbackFile.file.field.name,)
        help_text = {
            models.FeedbackFile.file.field.name: (
                'При необходимоти прикрепите файлы'
            ),
        }
        widgets = {
            models.FeedbackFile.file.field.name: (
                django.forms.FileInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'file',
                        'allow_multiple_selected': True,
                    },
                )
            ),
        }


__all__ = [
    'FeedbackForm',
    'FeedbackAutherForm',
    'FeedbackFileForm',
]
