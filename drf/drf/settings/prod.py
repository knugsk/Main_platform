from .base import *
import environ

ALLOWED_HOSTS = ['*']

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('knugsk'),
        'USER': env('dbmasteruser'),
        'PASSWORD': env('gHdF]]D}*4*%oKwmif}X`G.xl+JWHT5V'),
        'HOST': env('ls-106dc883a1986d68760bf6aa897fd47f62dbc0ef.czfqvjekjmqe.ap-northeast-2.rds.amazonaws.com'),
        'PORT': '5432',
    }
}