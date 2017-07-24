import os

from setuptools import setup, find_packages

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(root_path, 'CHANGES.txt')) as f:
    CHANGES = f.read()

version = __import__('configfactory').get_version()

requires = [
    'django==1.10.3',
    'django-jsonfield==1.0.1',
    'django-autoslug==1.9.3',
    'dj-static==0.0.6',
    'pytz==2016.10',
    'requests==2.11.1',
    'jsonschema==2.5.1',
    'gunicorn==19.6.0',
    'apscheduler==3.3.0',
    'packaging==16.8',
]

setup(
    name='am-configfactory',
    version=version,
    description='Admiral Markets distributed configurations server',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
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
