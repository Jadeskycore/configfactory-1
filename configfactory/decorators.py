from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse

from configfactory import auth


def login_required():
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user = auth.get_user(request)
            if user is None:
                return redirect(to=reverse('login'))
            return func(request, *args, **kwargs)
        return inner
    return decorator
