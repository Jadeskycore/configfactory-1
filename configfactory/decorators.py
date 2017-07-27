from functools import wraps

from django.core.exceptions import PermissionDenied

from configfactory import auth


def login_required():
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user = auth.get_user(request)
            if user is None:
                raise PermissionDenied
            return func(request, *args, **kwargs)
        return inner
    return decorator
