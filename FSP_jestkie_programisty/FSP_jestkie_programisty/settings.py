'''
Django settings for FSP_jestkie_programisty project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
'''

from pathlib import Path

import os

import dotenv
from django.conf.global_settings import EMAIL_USE_TLS

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def load_bool(name, default):
    env_value = os.getenv(name, str(default).lower())
    return env_value in ('true', 'yes', '1', 'y', 't')

BASE_DIR = Path(__file__).resolve().parent.parent

MAIL = os.getenv('EMAIL', 'no-reply@feedback.ru')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='fds')

DEBUG = load_bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = MAIL
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', 'somepassword')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Application definition

INSTALLED_APPS = [
    'ajax.apps.AjaxConfig',
    'login.apps.LoginConfig',
    'about.apps.AboutConfig',
    'catalog.apps.CatalogConfig',
    'feedback.apps.FeedbackConfig',
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ckeditor_5',
    'sorl.thumbnail',
    'django_cleanup.apps.CleanupConfig',
]

SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'FSP_jestkie_programisty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ACCOUNT_EMAIL_UNIQUE = True

ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

WSGI_APPLICATION = 'FSP_jestkie_programisty.wsgi.application'

MAX_AUTH_ATTEMPTS = 3


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME', 'name'),
        'USER': os.getenv('USER', 'user'),
        'PASSWORD': os.getenv('PASSWORD', 'passw'),
        'HOST': 'localhost',
        'PORT': 5432,
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


LANGUAGES = [
    ('ru', 'Russian'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]


STATIC_ROOT = BASE_DIR / '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            'bulletedList',
            'numberedList',
            'blockQuote',
        ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph',
            'heading1',
            'heading2',
            'heading3',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': [
            'heading',
            '|',
            'outdent',
            'indent',
            '|',
            'bold',
            'italic',
            'link',
            'underline',
            'strikethrough',
            'code',
            'subscript',
            'superscript',
            'highlight',
            '|',
            'codeBlock',
            'sourceEditing',
            'insertImage',
            'bulletedList',
            'numberedList',
            'todoList',
            '|',
            'blockQuote',
            'imageUpload',
            '|',
            'fontSize',
            'fontFamily',
            'fontColor',
            'fontBackgroundColor',
            'mediaEmbed',
            'removeFormat',
            'insertTable',
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative',
                '|',
                'imageStyle:alignLeft',
                'imageStyle:alignRight',
                'imageStyle:alignCenter',
                'imageStyle:side',
                '|',
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ],
        },
        'table': {
            'contentToolbar': [
                'tableColumn',
                'tableRow',
                'mergeTableCells',
                'tableProperties',
                'tableCellProperties',
            ],
        },
        'heading': {
            'options': [
                {
                    'model': 'paragraph',
                    'title': 'Paragraph',
                    'class': 'ck-heading_paragraph',
                },
                {
                    'model': 'heading1',
                    'view': 'h1',
                    'title': 'Heading 1',
                    'class': 'ck-heading_heading1',
                },
                {
                    'model': 'heading2',
                    'view': 'h2',
                    'title': 'Heading 2',
                    'class': 'ck-heading_heading2',
                },
                {
                    'model': 'heading3',
                    'view': 'h3',
                    'title': 'Heading 3',
                    'class': 'ck-heading_heading3',
                },
            ],
        },
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        },
    },
}

EMAIL_FILE_PATH = BASE_DIR / 'send_mail/'

LOGIN_REDIRECT_URL = '/admin'

AUTHENTICATION_BACKENDS = [
    'login.backends.AuthBackend',
]

SECURE_CROSS_ORIGIN_OPENER_POLICY=None

SESSION_COOKIE_SECURE=False