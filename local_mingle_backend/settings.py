"""
Django settings for local_mingle_backend project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
location = lambda x: os.path.join(os.path.realpath(BASE_DIR), x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')_8!xzy%yia0v*+05_49vb9gucgi!sqfn%l7d(g1dyp)hq+fvr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    #3rd parth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'debug_toolbar',
    'ckeditor',
    'widget_tweaks',
    'ckeditor_uploader',
    'django_filters',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'import_export',
    'mptt',
    'django_mptt_admin',
    'social_django',
    'rest_social_auth',
    'sslserver',
    'fcm_django',
    'django_crontab',
]

CUSTOM_APPS = [
    'accounts.apps.AccountsConfig',
    'event',
    'payment',
]

INSTALLED_APPS += CUSTOM_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'local_mingle_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'local_mingle_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Username field assign either email or mobile

USERNAME = "email"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    location('static'),
)
STATIC_ROOT = location('public/static')

MEDIA_URL = '/media/'
MEDIA_ROOT = location('public/media')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

LANGUAGES = (
    ('en', _('English')),
)


CKEDITOR_UPLOAD_PATH='upload/'
CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = ['127.0.0.1']


# *** stripe config start ***

STRIPE_PUBLIC_KEY = 'pk_test_51IsOlbSJfytDQt8mxA52OHmvXU8T4O7zHt9VTHQOzluURMASeYom8cZnOgYMStFTac4qf1FGEEHYy7ooaCUuyUob00JHsKwyXZ'
STRIPE_SECRET_KEY = 'sk_test_51IsOlbSJfytDQt8mWqloyUXBfkeUPCXmqkHoPEnRa6wIeHuBfa4eJD2ztSVYLDVo0ArHiDijM1DgcL5Wqx9vFDJF00Gzly4eng'

# *** stripe config end ***


# *** social auth settings start ***
SOCIAL_AUTH_FACEBOOK_KEY = '751188928882132'
SOCIAL_AUTH_FACEBOOK_SECRET = '741dd3e6c21db6c710da089b764e670d'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': ','.join([
        # 'public_profile',
        'id', 'cover', 'name', 'first_name', 'last_name', 'age_range', 'link',
        'gender', 'locale', 'picture', 'timezone', 'updated_time', 'verified',
        # extra fields
        'email',
    ]),
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    '90467052393-ud49796jibdqbcru8q38aia5vqfae5n5.apps.googleusercontent.com'


)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '92pW9KCL0mWKrYY4-9D0x2Nz'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', ]

# *** social auth settings end ***

TWILIO_ACCOUNT_SID = 'ACbfe0cd41ed4784bd87a52c2bc82afeaa'
TWILIO_AUTH_TOKEN = '7e281b8730edd965bb151031d95ad121'


# *** paypal config start ***

# PAYPAL_CLIENT_ID = 'AekPd_mXXFSb9BHNmPRUkWOHRW3dk99vBgYBNZtSdIXclTOMyvdPVxkJ_Z_Gtohs_PzX52bQE7SQFRGD'
# PAYPAL_CLIENT_SECRET = 'EFwsGaJA9foAq3Ok6-3a_vbd3V3786FtZ_CZtSyegOu94C4jpFCYTYuvHFKT5-ywv8j5IB2_lVOKwiKj'

PAYPAL_CLIENT_ID = 'AQleVRc9Wsly3JL330EfmSixQrhG4nwUA7QVTtvnUbHAm-4ZkeZMtGCU31qQwZMJf1XZR6w2v4vtFvQR'
PAYPAL_CLIENT_SECRET = 'EI4D8-y8qJSGR1jNzojA6hhQBo3z8NpCblQ3s13GcbxL6P1UZQwLYPyYhjG_x-85ZyjdDfSV1TaXDU5W'
# *** paypal config end ***

LOCAL_MINGLE_PRODUCT_LIST = ['Bronze', 'Silver', 'Gold']

# *** fcm-django settings start ***

FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": "AAAAn4zIwB4:APA91bH2LGJJcCqzhuQXaKOq26tog5GissVWJybqxKrlv98yIu-sLfzWY6wm2BHt48-89XUPHa_yKSGVsLV0mAdI32oWO5I9r8tcrOWWSDdCpDchLk9hJyl6whTeVy6ESySM79McNJP7"
}


# *** fcm-django settings end ***

# *** Cron-Job settings start ***

CRONJOBS = [
    ('30 4 * * *', 'event.management.commands.event_sync_ticketmaster', '>> event_sync.log')
]

# *** Cron-Job settings end ***

# *** Sentry settings start ***

import sentry_sdk
sentry_sdk.init(
    "https://8f8cea06f0d745af8c0f5f37363768ea@o361285.ingest.sentry.io/5937468",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# *** Sentry settings end ***

try:
    from local_mingle_backend.settings_sgspl import *
    from local_mingle_backend.settings_local import *
except ImportError:
    pass


