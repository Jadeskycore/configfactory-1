from configfactory.support.versioning import get_version

# Set public version
VERSION = '0.35dev'
__version__ = get_version(VERSION)

default_app_config = 'configfactory.apps.ConfigFactoryConfig'
