from django.test import TestCase

from configfactory.models import Component


class ModelsTestCase(TestCase):

    def test_component_environment_settings_fields(self):

        component = Component()
        component.name = 'Database'
        component.alias = 'database'
        component.save()
