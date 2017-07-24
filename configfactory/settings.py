import os

from configfactory import paths

ALLOWED_HOSTS = ['*']

SECRET_KEY = '28$0ld^(u&7o%f_e4sqh@rl&lere4kzsca#@&6@f+#5k7r963b'

DEBUG = True

ROOT_URLCONF = 'configfactory.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(paths.BASE_ROOT, 'db.sqlite3'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(paths.APP_ROOT, 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'configfactory.context_proccessors.components',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

INSTALLED_APPS = [
    'configfactory',
    'django.contrib.staticfiles',
]

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = (
    os.path.join(paths.APP_ROOT, 'static'),
)

ENVIRONMENTS = [
    'development',
    'staging',
    'production'
]

TIME_ZONE = 'UTC'
