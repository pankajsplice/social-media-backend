from pathlib import Path
import os
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'sgsplbase',
#         'USER': 'admin',
#         'PASSWORD': 'vishnu',
#         'HOST': '127.0.0.1',
#         'PORT': '',
#     }
# }
#
HTML_MINIFY = False

CACHE_TTL = 60 * 60
CACHE_TTL = 0
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
SECRET_KEY = 'hku6ome=wozp1*bll^-^9g00rlus8n2fvsqi-5lai$6p*%4ioa'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
