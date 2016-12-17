import multiprocessing
from multiprocessing import Process

from django.conf import settings
from django.core.management.base import BaseCommand

from am.configfactory.wsgi import WSGIApplication


class Command(BaseCommand):

    help = 'Run Config Factory application.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
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

    def handle(self, *args, **options):

        # Set debug mode
        debug = options['debug']

        # Set settings
        settings.DEBUG = debug

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
        wsgi_app = WSGIApplication(options=options)

        # Create wsgi application process
        wsgi_app_process = Process(target=wsgi_app.run)
        wsgi_app_process.start()

        # Initialize cron worker
        # cron_app = CronApplication()

        # Create and start cron application process
        # cron_app_process = Process(target=cron_app.run)
        # cron_app_process.start()

        # Run multiple processes
        try:
            wsgi_app_process.join()
        #     cron_app_process.join()
        except (KeyboardInterrupt, SystemExit):
            print('Shot down signal received...')
