import os

from setuptools import setup, find_packages

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(root_path, 'CHANGES.txt')) as f:
    CHANGES = f.read()
try:
    with open(os.path.join(root_path, 'version.txt')) as f:
        VERSION = f.read()
except FileNotFoundError:
    VERSION = 'dev'

requires = [
    'pytest-runner',
    'django==1.10.1',
    'tornado==4.4.2',
    'django-jsonfield==1.0.1',
    'django-autoslug==1.9.3',
    'pytz==2016.6.1',
    'requests==2.11.1',
    'jsonschema==2.5.1'
]

setup(
    name='am-configfactory',
    version=VERSION,
    description='Admiral Markets distributed configurations server',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires + [
        'pytest'
    ],
    entry_points="""\
    [console_scripts]
    configfactory = am.configfactory.runner:main
    """,
)
