from configfactory.settings import *

LOGGING = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

ENVIRONMENTS = [
    {
        'alias': 'development'
    },
    {
        'alias': 'testing'
    }
]
