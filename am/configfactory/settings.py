import os

from am.configfactory import APP_ROOT, BASE_ROOT, DATA_ROOT

ALLOWED_HOSTS = ['*']

SECRET_KEY = '28$0ld^(u&7o%f_e4sqh@rl&lere4kzsca#@&6@f+#5k7r963b'

DEBUG = True

ROOT_URLCONF = 'am.configfactory.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_ROOT, 'db.sqlite3'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_ROOT, 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'am.configfactory.context_proccessors.components',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'am.configfactory.middleware.BasicAuthMiddleware',
]

INSTALLED_APPS = [

    'am.configfactory',
]

ENVIRONMENTS = [
    'development',
    'staging',
    'production'
]

BACKUP_ROOT = DATA_ROOT

BACKUP_PERIOD = 10  # seconds

BACKUP_COUNT = 10  # seconds

AUTH_ENABLED = True

AUTH_USERNAME = 'admin'

AUTH_PASSWORD = 'password'
