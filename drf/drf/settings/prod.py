from .base import *
import environ, django

from django.core import *

ALLOWED_HOSTS = ['*']

DEBUG = False

env = environ.Env()
environ.Env.read_env('/home/ubuntu/Main_platform/drf/drf/.env')
AWS_STORAGE_BUCKET_NAME='bucket-xgthnf'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}

from .aws import *

if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE='drf.settings.aws.AwsMediaStorage'
    STATICFILES_STORAGE='drf.settings.aws.AwsStaticStorage'
    AWS_QUERYSTRING_AUTH=False
