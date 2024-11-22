import uuid

import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.safestring
import django.utils.timezone
import django_ckeditor_5.fields
import sorl.thumbnail

import catalog.validators
import core.models


def item_directory_path(instance, filename):
    return f'catalog/{instance.item.id}/{uuid.uuid4()}-{filename}'


class Category(core.models.Core):
    slug = django.db.models.SlugField(
        'слаг',
        unique=True,
        max_length=200,
        help_text='Только латинцкие буквы, цифры и знааки _ и -',
    )
    weight = django.db.models.IntegerField(
        'порядок (чем меньше, тем выше)',
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

        def __str__(self):
            return self.name[:15]


class Tag(core.models.Core):
    slug = django.db.models.SlugField(
        'Слаг',
        unique=True,
        max_length=200,
        help_text='Только латинцкие буквы, цифры и знааки _ и -',
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

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

    discipline = django.db.models.ForeignKey(
        'category',
        on_delete=django.db.models.CASCADE,
        verbose_name='Дисциплина',
        help_text='Выберите дисциплину',
        related_name='catalog_disciplene',
        unique=False,
        null=True,
    )
    program = django_ckeditor_5.fields.CKEditor5Field(
        'программа',
        help_text=('Опишите что будет происходить'),
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
        'category',
        on_delete=django.db.models.CASCADE,
        verbose_name='Страна',
        help_text='Выберите Страна',
        related_name='catalog_country',
        unique=False,
        null=True,
    )
    subject = django.db.models.ForeignKey(
        'category',
        on_delete=django.db.models.CASCADE,
        verbose_name='Субъект',
        help_text='Выберите субект',
        related_name='catalog_subject',
        unique=False,
        null=True,
    )
    town = django.db.models.ForeignKey(
        'category',
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
    )

    def __str__(self):
        return self.name[:15]

    def image_tmb(self):
        if self.main_image.image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.main_image.get_image_50x50.url}">',
            )

        return 'Нет изображения'

    image_tmb.short_description = 'превью'
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
        default_related_name = 'items'

        def __str__(self):
            return self.name[:15]


class ImageBaseModel(django.db.models.Model):
    image = django.db.models.ImageField(
        'изображение',
        upload_to=item_directory_path,
        default=None,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            '300x300',
            crop='center',
            quality=51,
        )

    @property
    def get_image_50x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            '50x50',
            crop='center',
            quality=51,
        )

    def __str__(self):
        return self.item.name

    class Meta:
        abstract = True


class MainImage(ImageBaseModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name='main_image',
    )

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'главное изображение'
        verbose_name_plural = 'главные изображения'

        def __str__(self):
            return self.name[:15]


class Image(ImageBaseModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name='images',
    )

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'

        def __str__(self):
            return self.name[:15]


__all__ = [
    'Category',
    'Tag',
    'Item',
    'ImageBaseModel',
    'MainImage',
    'Image',
    'ItemManager',
]
