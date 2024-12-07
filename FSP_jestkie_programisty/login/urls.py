from tempfile import template

import django.contrib.auth.views
import django.urls

import login.views

app_name = 'auth'

urlpatterns = [
    django.urls.path('login/',
         django.contrib.auth.views.LoginView.as_view(
             template_name='registration/login.html',
         ),
         name='login',
    ),
    django.urls.path(
        'logout/',
        django.contrib.auth.views.LogoutView.as_view(
            template_name='registration/logout.html',
        ),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done/',
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html',
        ),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset/',
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    django.urls.path(
        'reset/<uidb64>/<token>/',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'reset/done/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    django.urls.path(
        'profile/',
        login.views.profile,
        name='profile',
    ),
    django.urls.path(
        'signup/',
        login.views.signup,
        name='signup',
    ),
    django.urls.path(
        'confirm/<int:pk>',
        login.views.confirm,
        name='confirm',
    ),
    django.urls.path(
        'reactivate/<int:pk>/',
        login.views.reactivate,
        name='reactivate',
    ),
    django.urls.path(
        'user/list/',
        login.views.user_list,
        name='user_list'
    ),
    django.urls.path(
        'user/{int:pk}',
        login.views.user_detail,
        name='user_detail',
    ),
]
