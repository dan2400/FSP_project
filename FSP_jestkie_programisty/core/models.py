import re

import django.core.exceptions
import django.db.models
import transliterate

ONLY_LETTERS_REGEX = re.compile(r'[^\w]')


class PublishedManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)


class Core(django.db.models.Model):
    objects = PublishedManager()

    name = django.db.models.CharField(
        'название',
        help_text='Имя объекта',
        max_length=150,
    )
    is_published = django.db.models.BooleanField('опубликовано', default=True)

    canonical_name = django.db.models.CharField(
        max_length=150,
        null=True,
        default='default',
        unique=True,
        editable=True,
        verbose_name='каноническое имя',
        help_text='Каноническое название элемента',
    )

    def _name_gen(self):
        try:
            transliterated = transliterate.translit(
                self.name.lower(),
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = self.name.lower()

        return ONLY_LETTERS_REGEX.sub(
            '',
            transliterated,
        )

    def save(self, *args, **kwargs):
        self.canonical_name = self._name_gen()
        super().save(*args, **kwargs)

    def clean(self):
        self.canonical_name = self._name_gen()
        if (
            type(self)
            .objects.filter(canonical_name=self.canonical_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise django.core.exceptions.ValidationError(
                'Такое имя уже занято',
            )

    class Meta:
        abstract = True


__all__ = [
    'Core',
]
