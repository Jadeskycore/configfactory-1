from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$',
        view=views.components,
        name='api'),

    url(r'^backup/dump/$',
        view=views.backup_dump,
        name='api-backup-dump'),

    url(r'^backup/cleanup/$',
        view=views.backup_cleanup,
        name='api-backup-cleanup'),

    url(r'^(?P<environment>\w+)/$',
        view=views.components),

    url(r'^(?P<environment>\w+)/get/(?P<path>[-.\w\d]+)/$',
        view=views.components),

    url(r'^(?P<environment>\w+)/(?P<alias>[-\w\d]+)/$',
        view=views.component_settings,
        name='api-component'),

    url(r'^(?P<environment>\w+)/(?P<alias>[-\w\d]+)/get/(?P<path>[-.\w\d]+)/$',
        view=views.component_settings),
]
