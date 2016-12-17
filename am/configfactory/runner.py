import argparse
import os
import sys
from django.utils import timezone
from django.conf import settings
from django.core.management import call_command
from django.core.urlresolvers import reverse

from am.configfactory import DATA_ROOT


def main_(as_module=False):

    this_module = __package__ + '.main'

    if as_module:
        name = 'python -m ' + this_module
        sys.argv = ['-m', this_module] + sys.argv[1:]
    else:
        name = None

    parser = argparse.ArgumentParser(description='ConfigFactory server.', prog=name)
    parser.add_argument('--host', default='127.0.0.1', help='Server host')
    parser.add_argument('--port', default='4444', help='Server port')
    parser.add_argument('--backup_dir', default=DATA_ROOT, help='Backup dir')
    parser.add_argument('--backup', dest='backup', action='store_true', help='Use backup service', default=False)
    parser.add_argument('--backup_period', type=int, help='Backup period (seconds)', default=10)
    parser.add_argument('--backup_count', type=int, help='Backup count', default=10)
    parser.add_argument('--debug', dest='debug', action='store_true', default=False)
    parser.add_argument('--reload', dest='reload', action='store_true', default=False)
    parser.add_argument('--auth', dest='auth', action='store_true', help='Use authentication', default=False)
    parser.add_argument('--auth_username', default='admin', help='Username')
    parser.add_argument('--auth_password', default='pass', help='Password')
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'am.configfactory.settings')

    host = args.host
    port = args.port
    debug = args.debug
    reload = args.reload
    auth = args.auth
    auth_username = args.auth_username
    auth_password = args.auth_password
    backup = args.backup
    backup_period = args.backup_period
    backup_count = args.backup_count
    backup_dir = args.backup_dir

    # Overwrite django settings
    settings.DEBUG = debug
    settings.AUTH_ENABLED = auth
    settings.AUTH_USERNAME = auth_username
    settings.AUTH_PASSWORD = auth_password
    settings.BACKUP_DIR = backup_dir
    settings.BACKUP_PERIOD = backup_period
    settings.BACKUP_COUNT = backup_count

    # wsgi_application = tornado.wsgi.WSGIContainer(get_wsgi_application())

    call_command('migrate')

    if not os.path.exists(backup_dir):
        raise RuntimeError("Backup directory `{}` does not exist.".format(backup_dir))

    print('====== Starting ConfigFactory server {}:{} ======'.format(host, port))
    print('Server parameters:')
    print('debug: {}'.format(debug))
    print('reload: {}'.format(reload))
    print('auth: {}'.format(auth))
    print('backup: {}'.format(backup))
    print('backup period: every {} seconds'.format(backup_period))
    print('backup count: {}'.format(backup_count))
    print('backup dir: {}'.format(backup_dir))
    print('current time: {}'.format(timezone.get_current_timezone_name()))

    # http_server.listen(port=port, address=host)

    if backup:

        backup_url = 'http://{host}:{port}{path}'.format(host=host, port=port, path=reverse('api-backup-dump'))
        backup_cleanup_url = 'http://{host}:{port}{path}'.format(host=host, port=port,
                                                                 path=reverse('api-backup-cleanup'))
        request_params = {}

        if auth:
            request_params.update({
                'auth_mode': 'basic',
                'auth_username': auth_username,
                'auth_password': auth_password,
            })

        # @gen.coroutine
        # def auto_backup():
        #     logger.info("Starting data backup.")
        #     http_client = AsyncHTTPClient()
        #     try:
        #         yield http_client.fetch(backup_url, method='POST', body=b'', **request_params)
        #         yield http_client.fetch(backup_cleanup_url, method='POST', body=b'', **request_params)
        #         raise gen.Return
        #     except tornado.httpclient.HTTPError as e:
        #         logger.warning('Backup error: {}'.format(str(e)))

        # timer = tornado.ioloop.PeriodicCallback(auto_backup, backup_period * 1000)

        print('====== Starting backup service ======')
        # timer.start()

    # tornado.ioloop.IOLoop.current().start()


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "am.configfactory.settings")
    from django.core.management import execute_from_command_line
    sys.argv.insert(1, 'run')
    execute_from_command_line(sys.argv)
