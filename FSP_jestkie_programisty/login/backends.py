import django.conf
import django.contrib.auth.backends
import django.urls
import django.utils

import login.models

class AuthBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwagrs):
        try:
            if '@' in username:
                user = login.models.User.objects.by_mail(username)
            else:
                user = login.models.User.objects.get(username=username)
        except login.models.User.DoesNotExist:
            return None
        else:
            if user.ckeck_password(password):
                login.profile.attempts_count = 0

                login.profile.save()
                return user
            else:
                user.profile.attempts_count += 1
                if (
                    user.profile.attempts_count
                    >= django.conf.settings.MAX_AUTH_ATTEMPTS
                ):
                    user.is_active = False
                    user.profile.block_date = django.utils.timezone.now()
                    user.save()
                    activate_url = django.utils.reverse(
                        'auth:reactivate', kwagrs={'pk': user.id}
                    )

                    django.core.mail.send_mail(
                        f'Привет {user.username}',
                        'Мы заметили подозрительную активность.'
                        'Из-за этого заблокировали аккаунт.'
                        'Для разблокировки пройдите по ссылке'
                        '(действительная в тесении недели): '
                        f'{activate_url}',
                        django.conf.settings.MAIL,
                        [user.email],
                        fail_silently=False,
                    )
                user.profile.save()
        return None
