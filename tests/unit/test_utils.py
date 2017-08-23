from django.test import TestCase

from configfactory.exceptions import CircularInjectError
from configfactory.utils import inject_params


class UtilsTestCase(TestCase):

    def test_inject_param(self):

        data = "a = ${param:a}"

        self.assertEqual(
            inject_params(data, params={
                'a': 'TEST'
            }),
            "a = TEST"
        )

    def test_inject_params(self):

        data = (
            "a.b.c = ${param:a.b.c}, b.c = ${param:b.c}, "
            "c.d.e = ${param:c.d.e}"
        )

        self.assertEqual(
            inject_params(data, params={
                'a.b.c': 'ABC',
                'b.c': '${param:a.b.c}:BC',
                'c.d': 'CD',
                'c.d.e': '${param:b.c}:${param:c.d}',
            }),
            "a.b.c = ABC, b.c = ABC:BC, c.d.e = ABC:BC:CD"
        )

    def test_inject_params_to_self_component(self):

        data = (
            "db.host = ${param:db.host}, "
            "db.default.host = ${param:db.host}"
        )

        self.assertEqual(
            inject_params(data, params={
                'db.host': 'localhost',
                'db.default.host': '${param:db.host}',
            }),
            "db.host = localhost, db.default.host = localhost"
        )

    def test_inject_params_to_each_other(self):

        data = (
            "a.a = ${param:a.a}, a.b = ${param:a.b}, "
            "b.a = ${param:b.a}, b.b = ${param:b.b}"
        )

        self.assertEqual(
            inject_params(data, params={
                'a.a': 'AA',
                'a.b': '${param:b.b}',
                'b.a': '${param:a.b}',
                'b.b': 'BB',
            }),
            'a.a = AA, a.b = BB, b.a = BB, b.b = BB'
        )

    def test_circular_inject_params(self):

        data = (
            "a.a = ${param:a.a}, "
            "b.a = ${param:b.a}"
        )

        with self.assertRaises(CircularInjectError):
            inject_params(data, params={
                'a.a': '${param:b.a}',
                'b.a': '${param:a.a}',
            })

    def test_circular_inject_params_to_self(self):

        data = "a.a = ${param:a.a}"

        with self.assertRaises(CircularInjectError):
            inject_params(data, params={
                'a.a': '${param:a.a}',
            })
