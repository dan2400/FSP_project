import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.safestring
import django.utils.timezone
import django_ckeditor_5.fields
import core.models


def item_directory_path(instance, filename):
    return f'catalog/{instance.item.id}/{uuid.uuid4()}-{filename}'


class Town(core.models.Core):
    params = django.db.models.CharField(
        unique=False,
        null=True,
    )
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

        def __str__(self):
            return self.name[:15]


class Subject(core.models.Core):
    town = django.db.models.ManyToManyField(Town)
    class Meta:
        verbose_name = 'Субъект'
        verbose_name_plural = 'Субъекты'

        def __str__(self):
            return self.name[:15]


class Country(core.models.Core):
    subject = django.db.models.ManyToManyField(Subject)
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

        def __str__(self):
            return self.name[:15]


class Gender(core.models.Core):
    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

        def __str__(self):
            return self.name[:15]


class Age(core.models.Core):
    class Meta:
        verbose_name = 'Возраст'
        verbose_name_plural = 'Возраста'

        def __str__(self):
            return self.name[:15]


class Mass(core.models.Core):
    mass_start = django.db.models.IntegerField(
        unique=False,
        null=True,
        validators=[
            django.core.validators.MinValueValidator(10),
            django.core.validators.MaxValueValidator(1000),
        ],
    )
    mass_end = django.db.models.IntegerField(
        unique=False,
        null=True,
        validators=[
            django.core.validators.MinValueValidator(10),
            django.core.validators.MaxValueValidator(700),
        ],
    )
    class Meta:
        verbose_name = 'Весовая категория'
        verbose_name_plural = 'Весовые котегории'

        def __str__(self):
            return self.name[:15]


class Genage(core.models.Core):
    age = django.db.models.ForeignKey(
        'age',
        on_delete=django.db.models.CASCADE,
        verbose_name='Возраст',
        help_text='Выберите Возраст',
        related_name='catalog_age',
        unique=False,
        null=True,
    )
    gender = django.db.models.ForeignKey(
        'gender',
        on_delete=django.db.models.CASCADE,
        verbose_name='Пол',
        help_text='Выберите Пол',
        related_name='catalog_gen',
        unique=False,
        null=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

        def __str__(self):
            return self.name[:15]


class Discipline(core.models.Core):
    gen_age = django.db.models.ManyToManyField(Genage)
    mass_cat = django.db.models.ManyToManyField(Mass)

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

        def __str__(self):
            return self.name[:15]


def filter_select(obj):
    return (
        obj.filter(
            is_published=True,
            category__is_published=True,
        )
        .select_related(
            Item.category.field.name,
            Item.main_image.related.name,
        )
        .prefetch_related(
            django.db.models.Prefetch(
                Item.tags.field.name,
                queryset=Tag.objects.published().only(
                    Tag.name.field.name,
                ),
            ),
        )
    )


class Range_m(core.models.Core):
    class Meta:
        verbose_name = 'Маштаб'
        verbose_name_plural = 'Маштабы'

        def __str__(self):
            return self.name[:15]


class Sport(core.models.Core):
    discipline = django.db.models.ManyToManyField(
        'discipline',
        verbose_name='Дисциплина',
        help_text='Выберите дисциплину',
        related_name='catalog_sport',
        unique=False,
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Time(core.models.Core):
    start = django.db.models.DateTimeField(
        'время начала',
        unique=False,
        null=True,
    )
    end = django.db.models.DateTimeField(
        'время конца',
        unique=False,
        null=True,
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'время'
        verbose_name_plural = 'времена'


def order_only(obj):
    return (
        obj.order_by(
            f'{Item.category.field.name}__{Category.name.field.name}',
            Item.name.field.name,
        )
        .only(
            Item.name.field.name,
            Item.text.field.name,
            Item.main_image.related.name,
            f'{Item.category.field.name}__{Category.name.field.name}',
            f'{Item.tags.field.name}__{Tag.name.field.name}',
        )
    )


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            order_only(filter_select(self.get_queryset()))
        )

    def on_main(self):
        return (
            self.get_queryset()
            .filter(
                is_on_main=True,
            )
            .order_by(
                Item.name.field.name,
            )
        )


class Item(core.models.Core):
    objects = ItemManager()

    sport = django.db.models.ForeignKey(
        'discipline',
        on_delete=django.db.models.CASCADE,
        verbose_name='Дисциплина',
        help_text='Выберите дисциплину',
        related_name='catalog_item',
        unique=False,
        null=True,
    )
    created = django.db.models.DateTimeField(
        'время создания',
        auto_now_add=True,
        unique=False,
        null=True,
    )
    location = django.db.models.CharField(
        unique=False,
        null=True,
    )
    country = django.db.models.ForeignKey(
        'country',
        on_delete=django.db.models.CASCADE,
        verbose_name='Страна',
        help_text='Выберите Страна',
        related_name='catalog_country',
        unique=False,
        null=True,
    )
    subject = django.db.models.ForeignKey(
        'subject',
        on_delete=django.db.models.CASCADE,
        verbose_name='Субъект',
        help_text='Выберите субект',
        related_name='catalog_subject',
        unique=False,
        null=True,
    )
    town = django.db.models.ForeignKey(
        'town',
        on_delete=django.db.models.CASCADE,
        verbose_name='Город',
        help_text='Выберите город',
        related_name='catalog_town',
        unique=False,
        null=True,
    )
    number = django.db.models.IntegerField(
        unique=False,
        null=True,
        validators=[
            django.core.validators.MinValueValidator(10),
        ]
    )
    served = django.db.models.IntegerField(
        unique=False,
        null=True,
        validators=[
            django.core.validators.MaxValueValidator(700),
            django.core.validators.MinValueValidator(10),
        ]
    )
    time = django.db.models.ForeignKey(
        'time',
        on_delete=django.db.models.CASCADE,
        verbose_name='Время',
        help_text='Выберите Время',
        related_name='catalog_time',
        unique=False,
        null=True,
    )
    alert = django_ckeditor_5.fields.CKEditor5Field(
        'предупреждение',
        help_text=('Опишите что нужно делать'),
        unique=False,
        null=True,
    )
    range_m = django.db.models.ForeignKey(
        'range_m',
        on_delete=django.db.models.CASCADE,
        verbose_name='Страна',
        help_text='Выберите Страна',
        related_name='catalog_range_m',
        unique=False,
        null=True,
    )
    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
        default_related_name = 'items'

        def __str__(self):
            return self.name[:15]


__all__ = [
    'Category',
    'Tag',
    'Item',
    'Country'
]
