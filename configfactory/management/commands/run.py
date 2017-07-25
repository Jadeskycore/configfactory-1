import multiprocessing
from multiprocessing import Process

import dj_database_url
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from configfactory import backup, scheduler, wsgi
from configfactory.support.server import GunicornServer


class Command(BaseCommand):

    help = 'Run Config Factory application.'

    def add_arguments(self, parser):

        super().add_arguments(parser)

        parser.add_argument(
            '--bind',
            dest='bind',
            default='127.0.0.1:8000',
            help='The socket to bind.',
        )
        parser.add_argument(
            '--database_url',
            dest='database_url',
            help='Database url.',
            default='sqlite://'
        )
        parser.add_argument(
            '--use-static',
            action='store_true',
            default=True,
            help='Use static.',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Use debug.',
        )
        parser.add_argument(
            '--backup_interval',
            dest='backup_interval',
            type=int,
            help='Backup interval (seconds).',
            default=backup.BACKUP_INTERVAL
        )
        parser.add_argument(
            '--backup_count',
            dest='backup_count',
            type=int,
            help='Backup count.',
            default=backup.BACKUP_COUNT
        )
        parser.add_argument(
            '--backup_dir',
            dest='backup_dir',
            help='Backup directory.',
            default=backup.BACKUP_DIR
        )

    def handle(self, *args, **options):

        # Set debug mode
        debug = options['debug']

        # Set settings
        settings.DEBUG = debug
        settings.DATABASE = dj_database_url.config(options['database_url'])

        # Set backup settings
        backup.BACKUP_INTERVAL = options['backup_interval']
        backup.BACKUP_COUNT = options['backup_count']
        backup.BACKUP_DIR = options['backup_dir']

        # Migrate database
        call_command('migrate')

        # Create super user
        # if User.objects.count() == 0:
        #     call_command('createsuperuser')

        # Set server options
        options.update({
            'proc_name': 'configfactory',
        })

        # Set default debug options
        if debug:
            options['reload'] = True
        else:
            options['workers'] = multiprocessing.cpu_count() * 2 + 1

        # Initialize wsgi application
        server = GunicornServer(
            wsgi_app=wsgi.application,
            options=options
        )

        # Create wsgi application process
        server_process = Process(target=server.run)
        server_process.start()

        # Create and start cron application process
        scheduler_process = Process(target=scheduler.run)
        scheduler_process.start()

        # Run multiple processes
        try:
            server_process.join()
            scheduler_process.join()
        except (KeyboardInterrupt, SystemExit):
            print('Shot down signal received...')
