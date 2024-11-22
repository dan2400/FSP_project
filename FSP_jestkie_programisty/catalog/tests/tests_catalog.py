import django.test
from django.urls import reverse

import catalog.models


class StaticURLTests(django.test.TestCase):
    def setUp(self):
        self.category = catalog.models.Category.objects.create(
            is_published=True,
            name='Тестовая категория',
            slug='test-category-slug',
            canonical_name='kategotya',
            weight=100,
        )
        self.category2 = catalog.models.Category.objects.create(
            is_published=True,
            name='Тестовая категория2',
            slug='test-category-slug2',
            canonical_name='gor2',
            weight=100,
        )
        self.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='Тестовый тег',
            slug='test-tag-slug',
            canonical_name='tag',
        )
        self.tag2 = catalog.models.Tag.objects.create(
            is_published=True,
            name='Тестовый тег2',
            slug='test-tag-slug2',
            canonical_name='gad',
        )

        super(StaticURLTests, self).setUp()

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Category.objects.all().delete()

        super(StaticURLTests, self).tearDown()

    def test_catalog_endpoint(self):
        response = django.test.Client().get(reverse('catalog:item_list'))
        self.assertEqual(response.status_code, 200)


__all__ = []
