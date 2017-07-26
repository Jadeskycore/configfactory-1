from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.static import serve

from configfactory import backup
from configfactory.forms import (
    ComponentForm,
    ComponentSchemaForm,
    ComponentSettingsForm,
)
from configfactory.models import Component, environments


def index(request):
    return render(request, 'index.html')


def component_create(request):

    if request.method == 'POST':

        form = ComponentForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(to=reverse('index'))
    else:
        form = ComponentForm()

    return render(request, 'components/create.html', {
        'form': form
    })


def component_edit(request, alias):

    component = get_object_or_404(Component, alias=alias)

    if request.method == 'POST':

        form = ComponentForm(data=request.POST, instance=component)

        if form.is_valid():
            form.save()
            messages.success(request, "Component successfully updated.")
            return redirect(to=reverse('view_component',
                                       kwargs={'alias': component.alias}))
    else:
        form = ComponentForm(instance=component)

    return render(request, 'components/edit.html', {
        'form': form,
        'component': component
    })


def component_edit_schema(request, alias):

    component = get_object_or_404(Component, alias=alias)
    schema = component.schema

    if request.method == 'POST':

        form = ComponentSchemaForm(data=request.POST, initial={
            'schema': schema
        })

        if form.is_valid():
            data = form.cleaned_data
            component.schema = data['schema']
            component.save()
            messages.success(request, "Component schema successfully updated.")
    else:
        form = ComponentSchemaForm(initial={
            'schema': schema
        })

    return render(request, 'components/edit_schema.html', {
        'form': form,
        'component': component
    })


def component_delete(request, alias):

    component = get_object_or_404(Component, alias=alias)

    if request.method == 'POST':
        component.delete()
        messages.success(request, "Component successfully deleted.")
        return redirect(to=reverse('index'))

    return render(request, 'components/delete.html', {
        'component': component
    })


def component_view(request, alias, environment=None):

    component = get_object_or_404(Component, alias=alias)
    environment = environments.get_or_404(environment)

    try:
        readonly = int(request.GET.get('readonly', False))
    except TypeError:
        raise Http404

    settings_json = component.get_settings(
        environment=environment,
        flatten=readonly,
        raw_json=True
    )

    if request.method == 'POST':

        form = ComponentSettingsForm(
            require_schema=component.require_schema,
            schema=component.schema,
            data=request.POST,
            initial={
                'settings': settings_json
            }
        )

        if form.is_valid():
            data = form.cleaned_data
            component.set_settings(
                data=data['settings'],
                environment=environment.alias
            )
            component.save()
            messages.success(
                request,
                "Component settings successfully updated."
            )
        else:
            messages.error(
                request,
                form.errors.as_text(),
                extra_tags=' alert-danger'
            )

    else:
        form = ComponentSettingsForm(
            require_schema=component.require_schema,
            schema=component.schema,
            initial={
                'settings': settings_json
            })

    return render(request, 'components/view.html', {
        'component': component,
        'environments': environments,
        'current_environment': environment,
        'form': form,
        'readonly': readonly
    })


def backup_dump(request):

    if request.method == 'POST':

        name = backup.dump()

        messages.success(
            request,
            'Settings successfully dumped as `{}`.'.format(name)
        )
        return redirect(to=reverse('load_backup'))

    return render(request, 'backup/dump.html', {

    })


def backup_load(request, filename=None):

    if filename:

        if request.method == 'POST':
            backup.load(filename)
            messages.success(
                request, 'Backup `{}` successfully loaded.'.format(filename))
            return redirect(to=reverse('load_backup'))

        return render(request, 'backup/load_confirmation.html', {
            'filename': filename
        })

    backups = backup.get_all()

    return render(request, 'backup/load.html', {
        'backups': backups
    })


def backup_delete(request, filename):

    if not backup.exists(filename):
        raise Http404

    if request.method == 'POST':
        backup.delete(filename)
        messages.success(
            request,
            'Backup `{}` successfully deleted.'.format(filename))
        return redirect(to=reverse('load_backup'))

    return render(request, 'backup/delete.html')


def backup_serve(request, filename):

    if not backup.exists(filename):
        raise Http404

    return serve(
        request=request,
        path=filename,
        document_root=backup.BACKUP_DIR
    )
