import http

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):

    def test_homepage_endpoint(self):
        response = Client().get(reverse('main:main'))
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self):
        response = Client().get(reverse('main:coffee'))
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
        self.assertIn('Я чайник', response.content.decode('utf-8'))


__all__ = []
