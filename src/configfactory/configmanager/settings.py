from django.conf import settings


CONFIG_BACKEND = getattr(settings, 'CONFIG_BACKEND', {
    'CLASS': ''
})
