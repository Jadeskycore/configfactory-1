import os
import time

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone


def current_timestamp():
    return int(round(time.time() * 1000))


def dump():
    name = 'backup_{}.json'.format(current_timestamp())
    call_command('dumpdata', 'configfactory.Component', format='json',
                 output=os.path.join(settings.BACKUP_ROOT, name))
    return name


def cleanup(seconds=10):
    check_datetime = timezone.make_aware(timezone.now() - timezone.timedelta(seconds=seconds))
    backups = [b['name'] for b in get_all()[10:] if check_datetime > b['created_at']]
    for filename in backups:
        delete(filename)


def load(filename):
    call_command('loaddata', os.path.join(settings.BACKUP_ROOT, filename))


def exists(filename):
    return os.path.exists(os.path.join(settings.BACKUP_ROOT, filename))


def delete(filename):
    if exists(filename):
        os.remove(os.path.join(settings.BACKUP_ROOT, filename))


def get_all():
    backup_root = settings.BACKUP_ROOT
    return [
        {
            'name': filename,
            'size': os.path.getsize(os.path.join(backup_root, filename)),
            'created_at': timezone.datetime.fromtimestamp(os.path.getctime(os.path.join(backup_root, filename)),
                                                          tz=timezone.get_current_timezone())
        } for filename in sorted(os.listdir(backup_root), reverse=True)
        if os.path.isfile(os.path.join(backup_root, filename)) and filename.endswith('.json')
    ]
