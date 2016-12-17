from django.conf.urls import url, include

from am.configfactory import views


urlpatterns = [
    url(r'^$', view=views.index, name='index'),
    url(r'^backup/dump/$', view=views.backup_dump, name='backup-dump'),
    url(r'^backup/load/$', view=views.backup_load, name='backup-load'),
    url(r'^backup/load/(?P<filename>.+)/$', view=views.backup_load, name='backup-load'),
    url(r'^backup/delete/(?P<filename>.+)/$', view=views.backup_delete, name='backup-delete'),
    url(r'^components/create/$', view=views.component_create, name='components-create'),
    url(r'^components/(?P<alias>[-\w\d]+)/$', view=views.component_view, name='components-view'),
    url(r'^components/(?P<alias>[-\w\d]+)/edit/$', view=views.component_edit, name='components-edit'),
    url(r'^components/(?P<alias>[-\w\d]+)/edit/schema/$', view=views.component_edit_schema,
        name='components-edit-schema'),
    url(r'^components/(?P<alias>[-\w\d]+)/delete/$', view=views.component_delete, name='components-delete'),
    url(r'^components/(?P<alias>[-\w\d]+)/(?P<environment>\w+)/$', view=views.component_view,
        name='components-view'),

    url(r'^api/', include('am.configfactory.api.urls'))
]
