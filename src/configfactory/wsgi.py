import os

from django.core.wsgi import get_wsgi_application

from configfactory import paths

os.environ.setdefault("CONFIGFACTORY_CONFIG", paths.CONFIG_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configfactory.settings")

application = get_wsgi_application()
