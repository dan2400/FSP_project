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


class User(django.contrib.auth.models.User):
    object = UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):

    object = UserManager()

    def image_path(self, filename):
        return f'users/{self.user.id}/{filename}'

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    image = django.db.models.ImageField(
        'изображение',
        upload_to=image_path,
        null=True,
        blank=True,
        unique=False,
    )
    block_date = django.db.models.DateTimeField(
        'дата блокировки',
        blank=True,
        null=True,
    )
    attempts_count = django.db.models.PositiveIntegerField(
        'попыток входа',
        default=0,
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


class AddRequest(django.db.models.Model):
    object = UserManager()
    email = django.db.models.EmailField()

    class Meta:
        verbose_name = 'запрос'
        verbose_name_plural = 'запросы'
        default_related_name = 'addrequest'

        def __str__(self):
            return self.name[:15]
