import django.test
import parameterized

import catalog.models


class ModelsTests(django.test.TestCase):
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
        super(ModelsTests, self).setUp()

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Category.objects.all().delete()

        super(ModelsTests, self).tearDown()

    @parameterized.parameterized.expand(
        [
            ('Превосходное',),
            ('роскошное',),
            ('роско!шно',),
        ],
    )
    def test_item_val_fal(self, text):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Тестовый товар',
                category=self.category,
                canonical_name='testovaya',
                text=text,
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    @parameterized.parameterized.expand(
        [
            ('Превосходно',),
            ('роскошно',),
            ('роскошно!',),
        ],
    )
    def test_item_var_tr(self, text):
        item_count = catalog.models.Item.objects.count()

        self.item = catalog.models.Item(
            name='Тестовый товар',
            category=self.category,
            canonical_name='testovaya',
            text=text,
        )
        self.item.full_clean()
        self.item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
        )

    def test_item_length_ok(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Тестовый товар',
                category=self.category,
                canonical_name='testovaya',
                text='1' * 201,
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    # проверку на меньшее число не делаем, т.к. прошлые тесты в проверили это
    def test_item_caterogy(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Тестовый товар',
                category=self.category,
                canonical_name='testovaya',
                text='1' * 201,
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.item.tags.add(self.category2)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    def test_item_tag(self):
        item_count = catalog.models.Item.objects.count()

        self.item = catalog.models.Item(
            name='Тестовый товар',
            category=self.category,
            canonical_name='testovaya',
            text='роскошно',
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)
        self.item.tags.add(self.tag2)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
        )

    def test_teg_length(self):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.teg_t = catalog.models.Tag(
                is_published=True,
                name='Тестовый тег^2',
                canonical_name='testovaya',
                slug='_' * 201,
            )
            self.teg_t.full_clean()
            self.teg_t.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
        )

    @parameterized.parameterized.expand(
        [
            ('тест',),
            ('test_но_на_с_русским',),
            ('test with spaces',),
        ],
    )
    def test_teg_reg_tr(self, slug):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.teg_t = catalog.models.Tag(
                is_published=True,
                name='Тестовый тег^2',
                canonical_name='testovaya',
                slug=slug,
            )
            self.teg_t.full_clean()
            self.teg_t.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
        )

    @parameterized.parameterized.expand(
        [
            ('test', 'name'),
            ('test_with__', 'new'),
            ('test-with--', 'is'),
        ],
    )
    def test_tag_reg_fal(self, slug, name):
        tag_count = catalog.models.Tag.objects.count()
        self.tag_t = catalog.models.Tag(
            is_published=True,
            name=name,
            canonical_name=name,
            slug=slug,
        )
        self.tag_t.full_clean()
        self.tag_t.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 1,
        )

    def test_tag_unic(self):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag_t = catalog.models.Tag(
                is_published=True,
                name='Тестовый тег^2',
                canonical_name='testovaya',
                slug='test-tag-slug',
            )
            self.tag_t.full_clean()
            self.tag_t.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
        )

    def test_category_default(self):
        self.category_t = catalog.models.Category(
            is_published=True,
            name='Тестовая',
            canonical_name='testovaya',
            slug='test2',
        )
        self.category_t.full_clean()
        self.category_t.save()

        self.assertEqual(self.category_t.weight, 100)

    @parameterized.parameterized.expand(
        [
            (-100,),
            (0,),
            (64000,),
        ],
    )
    def test_category_weight_fal(self, weight):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category_t = catalog.models.Category(
                name='Тестовая категория',
                weight=weight,
                canonical_name='testovaya',
                slug='test2',
            )
            self.category_t.full_clean()
            self.category_t.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )

    @parameterized.parameterized.expand(
        [
            (100, 'kat'),
            (1, 'is'),
            (32000, 'my'),
        ],
    )
    def test_category_weight_tr(self, weight, name):
        category_count = catalog.models.Category.objects.count()
        self.category_t = catalog.models.Category(
            name=name,
            weight=weight,
            canonical_name=name,
            slug='test2',
        )
        self.category_t.full_clean()
        self.category_t.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            ('Новое',),
            ('Новое!',),
            ('Да, новое',),
        ],
    )
    def test_category_unic_tr(self, name):
        category_count = catalog.models.Category.objects.count()
        self.category_t = catalog.models.Category(
            name=name,
            weight=100,
            canonical_name='testovaya',
            slug='test2',
        )
        self.category_t.full_clean()
        self.category_t.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            ('Тестовaя категория',),
            ('Tестовая категория',),
            ('Тестоваякатегория',),
        ],
    )
    def test_category_unic_fal(self, name):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category_t = catalog.models.Category(
                name=name,
                weight=100,
                canonical_name='testovaya',
                slug='test2',
            )
            self.category_t.full_clean()
            self.category_t.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )


__all__ = []
