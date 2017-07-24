import logging
import os
import time

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from configfactory import paths

BACKUP_DIR = getattr(settings, 'BACKUP_DIR', paths.DATA_ROOT)

BACKUP_INTERVAL = getattr(settings, 'BACKUP_INTERVAL', 10)  # seconds

BACKUP_COUNT = getattr(settings, 'BACKUP_COUNT', 10)  # seconds

logger = logging.getLogger(__name__)


def current_timestamp():
    return int(round(time.time() * 1000))


def dump():

    logger.info("Running settings backup...")

    name = 'backup_{}.json'.format(current_timestamp())
    call_command('dumpdata', 'configfactory.Component', format='json',
                 output=os.path.join(BACKUP_DIR, name))
    return name


def cleanup():

    logger.info("Running settings backup cleanup...")

    dt_now = timezone.now()
    check_datetime = timezone.make_aware(
        dt_now - timezone.timedelta(seconds=BACKUP_INTERVAL))
    backups = [
        b['name']
        for b in get_all()[BACKUP_COUNT:]
        if check_datetime > b['created_at']
    ]
    for filename in backups:
        delete(filename)


def load(filename):
    call_command('loaddata', os.path.join(BACKUP_DIR, filename))


def exists(filename):
    return os.path.exists(os.path.join(BACKUP_DIR, filename))


def delete(filename):
    if exists(filename):
        os.remove(os.path.join(BACKUP_DIR, filename))


def get_all():
    return [
        {
            'name': filename,
            'size': os.path.getsize(os.path.join(BACKUP_DIR, filename)),
            'created_at': timezone.datetime.fromtimestamp(
                os.path.getctime(os.path.join(BACKUP_DIR, filename)),
                tz=timezone.get_current_timezone()
            )
        } for filename in sorted(os.listdir(BACKUP_DIR), reverse=True)
        if os.path.isfile(os.path.join(BACKUP_DIR, filename))
        and filename.endswith('.json')
    ]
