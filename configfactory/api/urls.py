from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$',
        view=views.components,
        name='api'),

    url(r'^(?P<environment>\w+)/$',
        view=views.components),
]
