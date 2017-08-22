from django.utils.module_loading import autodiscover_modules

from configfactory.support.versioning import get_version

# Set public version
VERSION = '0.35dev'
__version__ = get_version(VERSION)


def autodiscover():
    """
    Custom system autodiscover.
    """

    # Autodiscover signals subscribers
    autodiscover_modules('subscribers')

default_app_config = 'configfactory.apps.ConfigFactoryConfig'
