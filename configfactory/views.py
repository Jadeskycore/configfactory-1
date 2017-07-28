from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.static import serve

from configfactory import auth, backup
from configfactory.decorators import login_required, admin_required
from configfactory.exceptions import ComponentDeleteError
from configfactory.forms import (
    ComponentForm,
    ComponentSchemaForm,
    ComponentSettingsForm,
    LoginForm)
from configfactory.models import Component, environment_manager
from configfactory.services import (
    delete_component,
    get_all_settings,
    update_settings,
)
from configfactory.utils import inject_dict_params


@login_required()
def index(request):
    return render(request, 'index.html')


def login(request):

    if request.user:
        return redirect(to=reverse('index'))

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.user)
            return redirect(to=reverse('index'))
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form
    })


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@admin_required()
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


@admin_required()
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


@admin_required()
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
            messages.error(
                request,
                form.errors.as_text(),
                extra_tags=' alert-danger'
            )
    else:
        form = ComponentSchemaForm(initial={
            'schema': schema
        })

    return render(request, 'components/edit_schema.html', {
        'form': form,
        'component': component
    })


@admin_required()
def component_delete(request, alias):

    component = get_object_or_404(Component, alias=alias)

    if request.method == 'POST':
        try:
            delete_component(component)
        except ComponentDeleteError as e:
            messages.error(request, str(e), extra_tags=' alert-danger')
            return redirect(to=reverse('delete_component', kwargs={
                'alias': component.alias
            }))

        messages.success(request, "Component successfully deleted.")
        return redirect(to=reverse('index'))

    return render(request, 'components/delete.html', {
        'component': component
    })


@login_required()
def component_view(request, alias, environment=None):

    user = request.user
    component = get_object_or_404(Component, alias=alias)
    environments = environment_manager.all(user=user)
    environment = environment_manager.get_or_404(
        alias=environment,
        user=user
    )

    try:
        readonly = int(request.GET.get('readonly', False))
    except TypeError:
        raise Http404

    settings_dict = component.get_settings(
        environment=environment,
        flatten=readonly
    )

    if readonly:
        settings_dict = inject_dict_params(
            data=settings_dict,
            params=get_all_settings(environment, flatten=True),
            raise_exception=False
        )

    if request.method == 'POST':

        form = ComponentSettingsForm(
            component=component,
            environment=environment,
            data=request.POST,
            initial={
                'settings': settings_dict
            }
        )

        if form.is_valid():
            data = form.cleaned_data
            component = update_settings(
                component=component,
                environment=environment,
                data=data['settings']
            )
            messages.success(
                request,
                "Component %(component)s settings successfully updated." % {
                    'component': component.name
                }
            )
        else:
            messages.error(
                request,
                form.errors.as_text(),
                extra_tags=' alert-danger'
            )

    else:
        form = ComponentSettingsForm(
            component=component,
            environment=environment,
            initial={
                'settings': settings_dict
            }
        )

    return render(request, 'components/view.html', {
        'component': component,
        'environments': environments,
        'current_environment': environment,
        'form': form,
        'readonly': readonly
    })


@login_required()
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


@admin_required()
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


@admin_required()
def backup_delete(request, filename):

    if not backup.exists(filename):
        raise Http404

    if request.method == 'POST':
        backup.delete(filename)
        messages.success(
            request,
            'Backup `{}` successfully deleted.'.format(filename))
        return redirect(to=reverse('load_backup'))

    return render(request, 'backup/delete.html', {
        'filename': filename
    })


@admin_required()
def backup_serve(request, filename):

    if not backup.exists(filename):
        raise Http404

    return serve(
        request=request,
        path=filename,
        document_root=backup.BACKUP_DIR
    )
