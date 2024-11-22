from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):

    def test_about_endpoint(self):
        response = Client().get(reverse('about:about'))
        self.assertEqual(response.status_code, 200)


__all__ = []
