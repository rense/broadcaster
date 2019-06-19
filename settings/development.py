from settings import *

DEBUG = True
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]

SECRET_KEY = 'foo'

CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s module=%(module)s, '
                      'process_id=%(process)d, %(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'worker': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    },
}

DATABASE_DEFAULT = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'broadcaster',
    'USER': 'development',
    'PASSWORD': 'development',

    'HOST': '127.0.0.1',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
        'charset': 'utf8mb4'
    }
}

DATABASES = {
    'default': DATABASE_DEFAULT
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_ADDRESS = '{}:{}'.format(REDIS_HOST, REDIS_PORT)

DJANGO_REDIS_BACKEND_DB = 0
CELERY_REDIS_BACKEND_DB = 1

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}/{}".format(
            REDIS_ADDRESS, DJANGO_REDIS_BACKEND_DB
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
    'rest_framework.renderers.BrowsableAPIRenderer',
)

PID_DIR = '/tmp/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@localhost'
