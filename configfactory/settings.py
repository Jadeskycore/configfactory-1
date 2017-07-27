import os

import dj_database_url
from configfactory import paths
from configfactory.support import config

ALLOWED_HOSTS = ['*']

SECRET_KEY = '28$0ld^(u&7o%f_e4sqh@rl&lere4kzsca#@&6@f+#5k7r963b'

DEBUG = True

ROOT_URLCONF = 'configfactory.urls'

DATABASES = {
    'default': dj_database_url.config(
        env='CONFIGFACTORY_DATABASE_URL',
        default=config['database.url']
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.html',
            'auto_reload': True,
            'context_processors': [
                'configfactory.context_processors.auth',
                'configfactory.context_processors.components',
                'configfactory.context_processors.version',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'configfactory.middleware.auth_middleware'
]

INSTALLED_APPS = [
    'configfactory',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django_jinja',
]

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = (
    os.path.join(paths.APP_ROOT, 'static'),
)

TIME_ZONE = 'UTC'

ENVIRONMENTS = config.get('environments', [])

USERS = config.get('users', [])
