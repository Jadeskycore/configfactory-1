from django.conf.urls import url

from am.configfactory import views


urlpatterns = [
    url(r'^$', view=views.ui.index, name='index'),
    url(r'^backup/dump/$', view=views.ui.backup_dump, name='backup-dump'),
    url(r'^backup/load/$', view=views.ui.backup_load, name='backup-load'),
    url(r'^backup/load/(?P<filename>.+)/$', view=views.ui.backup_load, name='backup-load'),
    url(r'^backup/delete/(?P<filename>.+)/$', view=views.ui.backup_delete, name='backup-delete'),
    url(r'^components/create/$', view=views.ui.component_create, name='components-create'),
    url(r'^components/(?P<alias>[-\w\d]+)/$', view=views.ui.component_view, name='components-view'),
    url(r'^components/(?P<alias>[-\w\d]+)/edit/$', view=views.ui.component_edit, name='components-edit'),
    url(r'^components/(?P<alias>[-\w\d]+)/delete/$', view=views.ui.component_delete, name='components-delete'),
    url(r'^components/(?P<alias>[-\w\d]+)/(?P<environment>\w+)/$', view=views.ui.component_view,
        name='components-view'),

    url(r'^api/$', view=views.api.components, name='api'),
    url(r'^api/backup/dump/$', view=views.api.backup_dump, name='api-backup-dump'),
    url(r'^api/backup/cleanup/$', view=views.api.backup_cleanup, name='api-backup-cleanup'),
    url(r'^api/(?P<environment>\w+)/$', view=views.api.components),
    url(r'^api/(?P<environment>\w+)/get/(?P<path>[-.\w\d]+)/$', view=views.api.components),
    url(r'^api/(?P<environment>\w+)/(?P<alias>[-\w\d]+)/$', view=views.api.component_settings, name='api-component'),
    url(r'^api/(?P<environment>\w+)/(?P<alias>[-\w\d]+)/get/(?P<path>[-.\w\d]+)/$', view=views.api.component_settings),
]
