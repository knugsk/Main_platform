from .base import *
import environ, django

from django.core import *

ALLOWED_HOSTS = ['3.35.121.91', 'knugsk.com']
ACCESS_CONTROL_ALLOW_ORIGIN = ['*']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['https://3.35.121.91/', 'https://knugsk.com/']
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
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.{S3 리전}.amazonaws.com"
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {
        'ContentDisposition': 'attachment; filename="example.txt"',
        'ContentType': 'text/plain',
        'ContentEncoding': 'utf-8',  # UTF-8 인코딩 설정 추가
    }