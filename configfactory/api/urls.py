from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', view=views.components_view),

    url(r'^(?P<environment>\w+)/$', view=views.components_view),

    url(r'^(?P<environment>\w+)/(?P<alias>[-\w\d]+)/$',
        view=views.component_settings_view),
]
