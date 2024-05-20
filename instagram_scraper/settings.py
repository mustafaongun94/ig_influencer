from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CELERY_BROKER_REDIS_URL = "redis://localhost:6380"

DEBUG = True

CELERY_RESULT_BACKEND = "django-db"

CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL', default='redis://localhost:6379')

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

ALLOWED_HOSTS = ['*']


SECRET_KEY = 'django-insecure-!ww$&z$fj%lo=68eg(=*9rrl6*ve8317d-+krexy80e7x42kz5'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ig_scraper',
    'django_celery_beat',
    'django_celery_results',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'instagram_scraper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'instagram_scraper.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hyperiser',
        'USER': 'hyperiser',
        'PASSWORD': 'hyperiser',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AWS_ACCESS_KEY_ID = 'AKIA2Z2AWNCSVVCIUUIE'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'influencerfiles'
AWS_S3_SIGNATURE_NAME = 'S3V4'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
