from .base import *
import environ, django

from django.core import *

ALLOWED_HOSTS = ['3.35.121.91', 'knugsk.com']

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
    AWS_S3_SECURE_URLS = False      
    AWS_QUERYSTRING_AUTH = False   
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # Cache 설정 (선택 사항)
    'ContentDisposition': 'inline',  # 다운로드를 위한 설정 (선택 사항)
}

