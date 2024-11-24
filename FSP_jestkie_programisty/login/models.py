import sys

import django.contrib.auth.models
import django.db.models
import sorl.thumbnail

import catalog.models


if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    django.contrib.auth.models.User._meta.get_field('email')._unique = True

class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        'ya.ru': 'yandex.ru',
    }
    DOTS = {
        'yandex.ru': '-',
        'gmail.com': '',
    }

    def get_gueryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                django.contrib.auth.models.User.profile.related.name,
            )
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        normalized_email = self.normalize_email(mail)
        return self.active().get(email=normalized_email)

    @classmethod
    def normalize_email(cls, email):
        email = super().mormalize_email(email).lower()
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
            email_name, _ = email_name.split('+', 1)

            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)

            email_name = email_name.replace(
                '.', cls.DOTS.get(domain_part, '.')
            )
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email


class Profile(django.db.models.Model):
    def image_path(self, filename):
        return f'users/{self.user.id}/{filename}'

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    age = django.db.models.DateTimeField()
    gender = django.db.models.ForeignKey(
        catalog.models.Gender,
        on_delete=django.db.models.CASCADE,
        related_name='main_gender',
    )
    mass = django.db.models.IntegerField(
        validators=[
            django.core.validators.MinValueValidator(10),
            django.core.validators.MaxValueValidator(1000),
        ]
    )
    town = django.db.models.ForeignKey(
        catalog.models.Town,
        on_delete=django.db.models.CASCADE,
        related_name='main_town',
    )
    discipline = django.db.models.ManyToManyField(catalog.models.Discipline)
    is_active = django.db.models.BooleanField(default=True)
    records = django.db.models.ManyToManyField(catalog.models.Item)

    image = django.db.models.ImageField(
        'изображение',
        upload_to=image_path,
        null=True,
        blank=True,
    )

    def get_image_300x300(self):
        return sorl.thambnail.get_thumbnail(
            self.image,
            '300x300',
            crop='center',
            qualoty=5,
        )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
