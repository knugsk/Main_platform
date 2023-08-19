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
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.{S3 리전}.amazonaws.com"
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    
TEMPLATES[0]['APP_DIRS'] = False  # 애플리케이션별 템플릿 디렉토리 사용 안 함
TEMPLATES[0]['DIRS'] = [BASE_DIR / "static"]  # 템플릿 디렉토리 경로 설정

# 배포 환경에서는 개발자 도구를 비활성화하여 성능 향상을 도모합니다.
INSTALLED_APPS.remove('debug_toolbar')
MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')