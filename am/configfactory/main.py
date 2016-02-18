import argparse
import os
import sys
import logging
import tornado
import tornado.ioloop
import tornado.log
import tornado.wsgi
import tornado.httpserver
import tornado.web
import tornado.autoreload
from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

from am.configfactory import APP_ROOT, DATA_ROOT


def main(as_module=False):

    this_module = __package__ + '.main'

    if as_module:
        name = 'python -m ' + this_module
        sys.argv = ['-m', this_module] + sys.argv[1:]
    else:
        name = None

    parser = argparse.ArgumentParser(description='ConfigFactory server.', prog=name)
    parser.add_argument('--host', default='127.0.0.1', help='Server host')
    parser.add_argument('--port', default='4444', help='Server port')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False)
    parser.add_argument('--reload', dest='reload', action='store_true', default=False)
    parser.add_argument('--auth', dest='auth', action='store_true', default=False)
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'am.configfactory.settings')

    host = args.host
    port = args.port
    debug = args.debug
    reload = args.reload
    auth = args.auth

    settings.DEBUG = debug
    settings.AUTH_ENABLED = auth

    logging.basicConfig(level=logging.DEBUG)

    wsgi_application = tornado.wsgi.WSGIContainer(get_wsgi_application())

    call_command('migrate')

    if not os.path.exists(DATA_ROOT):
        os.makedirs(DATA_ROOT)

    tornado_application = tornado.web.Application(handlers=[
        (r'/backups/(.*)', tornado.web.StaticFileHandler, dict(path=DATA_ROOT)),
        (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_application)),
    ], static_path=os.path.join(APP_ROOT, 'static'), debug=debug, autoreload=reload)

    http_server = tornado.httpserver.HTTPServer(tornado_application)

    print('====== Starting ConfigFactory server {}:{} (debug={}, reload={}, auth={}) ======'.format(
        host, port, debug, reload, auth))
    http_server.listen(port=port, address=host)

    tornado.ioloop.IOLoop.current().start()
