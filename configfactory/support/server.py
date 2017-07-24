import gunicorn.app.base


class GunicornServer(gunicorn.app.base.BaseApplication):
    """
    Gunicorn WSGI server.
    """

    def __init__(self, wsgi_app, options=None):
        self.wsgi_app = wsgi_app
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
            return Cling(self.wsgi_app)
        return self.wsgi_app
