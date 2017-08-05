import os
import sys

from setuptools import setup, find_packages

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(root_path, 'CHANGES.txt')) as f:
    CHANGES = f.read()

sys.path.insert(0, os.path.join(root_path, 'src'))

version = __import__('configfactory').get_version()

requires = [
    'django==1.11.4',
    'django-jsonfield==1.0.1',
    'django-autoslug==1.9.3',
    'django-jinja==2.3.1',
    'dj-static==0.0.6',
    'dj-database-url==0.4.2',
    'pytz==2017.2',
    'jsonschema==2.6.0',
    'gunicorn==19.7.1',
    'apscheduler==3.3.1',
    'packaging==16.8',
    'appdirs==1.4.3',
    'pyyaml==3.12',
]

setup(
    name='am-configfactory',
    version=version,
    description='Distributed configurations server',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages('src', exclude=['tests']),
    package_dir={
        '': 'src',
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires + [
        'pytest',
        'pytest-django',
        'pytest-runner',
    ],
    entry_points="""\
    [console_scripts]
    configfactory = configfactory.runner:main
    """,
)
