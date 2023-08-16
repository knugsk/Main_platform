from .base import *
import environ

ALLOWED_HOSTS = ['*']

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

if AWS_S3_ACCESS_KEY_ID and AWS_S3_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # 장고 4.2부터 스토리지 클래스 지정방법이 변경되었습니다.
    STORAGES = {
        "default": {
            "BACKEND": "core.storages.aws.AwsMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "core.storages.aws.AwsStaticStorage",
        },
    }