from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from configfactory import views

urlpatterns = [

    url(r'^ping/$', view=views.ping, name='ping'),
    url(r'^alive/$', view=views.alive, name='alive'),

    url(r'^$', view=views.index, name='index'),

    url(r'^login/$',
        view=auth_views.login,
        name='login',
        kwargs={
            'template_name': 'login.html'
        }),

    url(r'^logout/$',
        view=auth_views.logout,
        name='logout',
        kwargs={
            'next_page': 'login'
        }),

    url(r'^components/create/$', view=views.component_create, name='new_component'),
    url(r'^components/(?P<alias>[-\w\d]+)/$', view=views.component_view, name='view_component'),
    url(r'^components/(?P<alias>[-\w\d]+)/edit/$',
        view=views.component_edit, name='edit_component'),
    url(r'^components/(?P<alias>[-\w\d]+)/edit/schema/$', view=views.component_edit_schema,
        name='edit_component_schema'),
    url(r'^components/(?P<alias>[-\w\d]+)/delete/$',
        view=views.component_delete, name='delete_component'),
    url(r'^components/(?P<alias>[-\w\d]+)/(?P<environment>\w+)/$', view=views.component_view,
        name='view_component_by_env'),

    url(r'^backup/dump/$', view=views.backup_dump, name='dump_backup'),
    url(r'^backup/load/$', view=views.backup_load, name='load_backup'),
    url(r'^backup/load/(?P<filename>.+)/$', view=views.backup_load, name='load_backup_file'),
    url(r'^backup/delete/(?P<filename>.+)/$', view=views.backup_delete, name='delete_backup'),
    url(r'^backup/serve/(?P<filename>.+)/$', view=views.backup_serve, name='serve_backup_file'),
    url(r'^logs/$', view=views.logs_index, name='logs'),
    url(r'^logs/serve/(?P<filename>.+)/$', view=views.logs_serve, name='serve_log_file'),
    url(r'^api/', include('configfactory.api.urls')),
]
