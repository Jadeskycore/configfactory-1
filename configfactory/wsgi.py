import gunicorn.app.base
from django.core.handlers.wsgi import WSGIHandler


class Application(gunicorn.app.base.BaseApplication):
    """
    WSGI application loader.
    """

    def __init__(self, handler=None, options=None):
        if handler is None:
            handler = WSGIHandler()
        self._handler = handler
        self.options = options or {}
        super().__init__()

    def init(self, parser, opts, args):
        pass

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        use_static = self.options.get('use_static')
        if use_static:
            from dj_static import Cling
            return Cling(self._handler)
        return self._handler
