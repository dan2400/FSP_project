import pathlib
import tempfile

import django.conf
import django.core.files.base
from django.test import Client, TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_name_label(self):
        name_label = type(self).form.fields['text'].label
        self.assertEqual(name_label, 'Сообщение')

    def test_name_help_text(self):
        name_help_text = type(self).form.fields['text'].help_text
        self.assertEqual(name_help_text, 'Место для сообщения')

    def test_create_task(self):
        feedback_count = Feedback.objects.count()
        form_data = {
            'name': 'Test',
            'text': 'Test',
            'mail': 'Test@Test.ru',
        }
        response = Client().post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse('feedback:feedback'))
        self.assertEqual(Feedback.objects.count(), feedback_count + 1)
        self.assertTrue(
            Feedback.objects.filter(
                auther__name='Test',
                text='Test',
                auther__mail='Test@Test.ru',
            ).exists(),
        )

    @django.test.override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory().name,
    )
    def test_file_upload(self):
        files = [
            django.core.files.base.ContentFile(
                f'file_{index}'.encode(),
                name='filename',
            )
            for index in range(10)
        ]
        form_data = {
            'name': 'Тест',
            'text': 'file_test',
            'mail': '123@l.com',
            'file': files,
        }
        django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        feedback_item = Feedback.objects.get(
            text='file_test',
        )
        self.assertEqual(feedback_item.files.count(), 10)
        feedback_files = feedback_item.files.all()
        media_root = pathlib.Path(django.conf.settings.MEDIA_ROOT)

        for index, file in enumerate(feedback_files):
            uploaded_file = media_root / file.file.path
            self.assertEqual(
                uploaded_file.open().read(),
                f'file_{index}',
            )


__all__ = []
