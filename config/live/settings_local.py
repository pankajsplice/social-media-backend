from pathlib import Path
import os

ALLOWED_HOSTS = ['localmingle.keycorp.in', '209.126.86.200','localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'localmingle',
        'USER': 'admin',
        'PASSWORD': '@dm!9098)(*',
        'HOST': '209.126.86.200',
        'PORT': '',
    }
}
