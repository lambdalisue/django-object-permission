#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
initialization django-object-permission

Add this backend to your ``AUTHENTICATION_BACKENDS`` like below::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'object_permission.backends.ObjectPermBackend',
    )

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.conf import settings
from django.db.models import get_models, signals
from django.contrib.auth.management import _get_permission_codename
from django.core.exceptions import ImproperlyConfigured

app_label = 'object_permission'
def set_default(name, value):
    setattr(settings, name, getattr(settings, name, value))

# Validate settings
if "%s.backends.ObjectPermBackend" % app_label not in settings.AUTHENTICATION_BACKENDS:
    raise ImproperlyConfigured("You have to set '%s.backends.ObjectPermBackend' to AUTHENTICATION_BACKENDS" % app_label)

# Set default settings
set_default(
    'OBJECT_PERMISSION_DEFAULT_HANDLER_CLASS', 
    'object_permission.handlers.base.ObjectPermHandler')
set_default('OBJECT_PERMISSION_EXTRA_DEFAULT_PERMISSIONS', ['view'])
set_default('OBJECT_PERMISSION_BUILTIN_TEMPLATETAGS', True)
set_default('OBJECT_PERMISSION_AUTODISCOVER', True)
set_default('OBJECT_PERMISSION_HANDLER_MODULE_NAME', 'ophandler')

# Load site (this must be after the default settings has complete)
from sites import site

# Regist templatetags for ObjectPermission
if settings.OBJECT_PERMISSION_BUILTIN_TEMPLATETAGS:
    from django.template import add_to_builtins
    add_to_builtins('%s.templatetags.object_permission_tags' % app_label)

# Add extra default permission
def _get_all_permissions(opts):
    "Returns (codename, name) for all permissions in the given opts."
    perms = []
    for action in settings.OBJECT_PERMISSION_EXTRA_DEFAULT_PERMISSIONS:
        perms.append((_get_permission_codename(action, opts), u'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms + list(opts.permissions)
def create_permissions(app, created_models, verbosity, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    app_models = get_models(app)
    if not app_models:
        return
    for klass in app_models:
        ctype = ContentType.objects.get_for_model(klass)
        for codename, name in _get_all_permissions(klass._meta):
            p, created = Permission.objects.get_or_create(codename=codename, content_type__pk=ctype.id,
                defaults={'name': name, 'content_type': ctype})
            if created and verbosity >= 2:
                print "Adding permission '%s'" % p
signals.post_syncdb.connect(create_permissions,
    dispatch_uid = "object_permission.management.create_permissions")

def autodiscover():
    """
    Auto-discover INSTALLED_APPS ophandler.py modules and fail silently when
    not present. This forces an import on them to register any handler bits they
    may want.
    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    handler_module_name = settings.OBJECT_PERMISSION_HANDLER_MODULE_NAME

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's object permission handler module.
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.%s' % (app, handler_module_name))
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            site._registry = before_import_registry

            # Decide wheter to bubble up this error. If the app just
            # doesn't have an object permission module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, handler_module_name):
                raise
if settings.OBJECT_PERMISSION_AUTODISCOVER:
    autodiscover()
