from .base import *
import environ

ALLOWED_HOSTS = ['*']

DEBUG = False

env = environ.Env()
environ.Env.read_env('/home/ubuntu/Main_platform/drf/drf/.env')

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

if env('AWS_S3_ACCESS_KEY_ID') and env('AWS_S3_SECRET_ACCESS_KEY') and env('AWS_STORAGE_BUCKET_NAME'):
    DEFAULT_FILE_STORAGE = "core.storages.aws.AwsMediaStorage"
    STATICFILES_STORAGE = "core.storages.aws.AwsStaticStorage"