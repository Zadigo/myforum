import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rfpn+3c*ftsqmn9c+=6*6pu5an97j5&4mvz^72wk^3csx(1@!)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'django_extensions',
    'django_celery_beat',
    'corsheaders',
    'drf_spectacular',
    'debug_toolbar',
    'import_export',
    'django_ckeditor_5',

    'allauth',
    'allauth.usersessions',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'api',
    'accounts',
    'forums',
    'threads',
    'notifications',
    'comments',
    'tags',
    'moderation',
    'polls'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'forum_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'forum_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.MyUser'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'


# Media

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Debug

INTERNAL_IPS = [
    '127.0.0.1'
]


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Cors
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000'
]


# RestFrameWork
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ['Token']
}


# Locales

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]


# Emailing

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_USE_LOCALTIME = True


# Sites

SITE_ID = 1


# Django All Auth for more information
# on the settings for django-allauth
# https://docs.allauth.org/en/latest/socialaccount/provider_configuration.html

# For two factor authentication, see:
# https://stackoverflow.com/questions/54908541/django-two-factor-authentication
# https://github.com/pyauth/pyotp?tab=readme-ov-file
# https://github.com/soldair/node-qrcode

USERSESSIONS_TRACK_ACTIVITY = False

SOCIALACCOUNT_FORMS = {
    'signup': 'accounts.forms.SocialSignupForm',
    'disconnect': 'accounts.forms.SocialLogoutForm',
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APPS': [
            {
                'client_id': '123',
                'secret': '456',
                'key': ''
            }
        ],
        # These are provider-specific settings that can only be
        # listed here:
        'SCOPE': [
            "profile",
            "email",
        ],
        'AUTH_PARAMS': {
            "access_type": "online",
        }
    }
}


# CKEditor for more information on customizing
# the editor https://pypi.org/project/django-ckeditor-5/

CKEDITOR_BASEPATH = MEDIA_ROOT / 'ckeditor/ckeditor'

CKEDITOR_UPLOAD_PATH = 'ck_editor/'

CKEDITOR_5_ALLOW_ALL_FILE_TYPES = False

CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg']

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic',
            'link', 'bulletedList'
        ]
    }
}


# Celery
# https://docs.celeryq.dev/en/stable/

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

if not DEBUG:
    # Use Redis as backend for caching instead of
    # the file system caching that we use for debugging

    REDIS_URL = f'redis://:{REDIS_PASSWORD}@redis:6379'

    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')

    RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER')

    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS')

    CELERY_BROKER_URL = 'amqp://{user}:{password}@rabbitmq:5672'.format(
        user=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD
    )

    CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@redis:6379'
else:
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'

    CELERY_RESULT_BACKEND = 'rpc://'


CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Oslo'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# Caching

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': BASE_DIR / 'cache'
        }
    }
else:
    CACHES = {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://:{REDIS_PASSWORD}@redis:6379',
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient"
        },
        'KEY_PREFIX': 'ecommerce'
    }


# HTTPS

if os.getenv('USES_HTTP_SCHEME', 'http') == 'https':
    SESSION_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_PROXY_SSL_HEADERSSL_REDIRECT = True
