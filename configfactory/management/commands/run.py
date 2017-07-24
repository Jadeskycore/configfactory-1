import multiprocessing
from multiprocessing import Process

from django.conf import settings
from django.core.management.base import BaseCommand

from configfactory import backup, scheduler, wsgi


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
            '--use-static',
            action='store_true',
            default=False,
            help='Use static.',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=settings.DEBUG,
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

        # Set backup settings
        backup.BACKUP_INTERVAL = options['backup_interval']
        backup.BACKUP_COUNT = options['backup_count']
        backup.BACKUP_DIR = options['backup_dir']

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
            options['use_static'] = True

        else:
            options['workers'] = multiprocessing.cpu_count() * 2 + 1

        # Initialize wsgi application
        wsgi_app = wsgi.Application(options=options)

        # Create wsgi application process
        wsgi_app_process = Process(target=wsgi_app.run)
        wsgi_app_process.start()

        # Create and start cron application process
        scheduler_process = Process(target=scheduler.run)
        scheduler_process.start()

        # Run multiple processes
        try:
            wsgi_app_process.join()
            scheduler_process.join()
        except (KeyboardInterrupt, SystemExit):
            print('Shot down signal received...')
