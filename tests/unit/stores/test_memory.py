from collections import OrderedDict

from django.test import TestCase

from configfactory.stores.memory import MemoryConfigStore


class MemoryConfigStoreTestCase(TestCase):

    def test_empty_store(self):

        store = MemoryConfigStore()

        self.assertDictEqual(store.all(), {})

    def test_get_and_update_store_data(self):

        store = MemoryConfigStore()

        self.assertDictEqual(store.all(), {})

        store.update('db', 'prod', OrderedDict([
            ('user', 'root'),
            ('pass', 'secret'),
        ]))

        store.update('redis', 'prod', OrderedDict([
            ('url', 'redis://127.0.0.1:5050/1'),
        ]))

        self.assertDictEqual(store.all(), {
            'db': {
                'prod': OrderedDict([
                    ('user', 'root'),
                    ('pass', 'secret'),
                ])
            },
            'redis': {
                'prod': OrderedDict([
                    ('url', 'redis://127.0.0.1:5050/1'),
                ])
            }
        })

        self.assertDictEqual(store.get('db', 'prod'), OrderedDict([
            ('user', 'root'),
            ('pass', 'secret'),
        ]))

        self.assertDictEqual(store.get('redis', 'prod'), OrderedDict([
            ('url', 'redis://127.0.0.1:5050/1'),
        ]))
