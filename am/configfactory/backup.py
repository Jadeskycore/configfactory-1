import os
import time
import pytz

from django.core.management import call_command
from django.utils import timezone

from am.configfactory import DATA_ROOT


def current_timestamp():
    return int(round(time.time() * 1000))


def dump():
    name = 'backup_{}.json'.format(current_timestamp())
    call_command('dumpdata', 'configfactory.Component', output=os.path.join(DATA_ROOT, name), indent=4)
    return name


def load(filename):
    call_command('loaddata', os.path.join(DATA_ROOT, filename))


def exists(filename):
    return os.path.exists(os.path.join(DATA_ROOT, filename))


def delete(filename):
    if exists(filename):
        os.remove(os.path.join(DATA_ROOT, filename))


def get_all():

    return [
        {
            'name': filename,
            'size': os.path.getsize(os.path.join(DATA_ROOT, filename)),
            'created_at': timezone.datetime.fromtimestamp(os.path.getctime(os.path.join(DATA_ROOT, filename)),
                                                          tz=pytz.timezone('UTC'))
        } for filename in sorted(os.listdir(DATA_ROOT), reverse=True) if os.path.isfile(os.path.join(DATA_ROOT, filename))
    ]
