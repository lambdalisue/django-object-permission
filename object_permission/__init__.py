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
from django.core.exceptions import ImproperlyConfigured

from settings import *
from autocmd.create_default_extra_permissions import *

from managers import manager

app_label = 'object_permission'

# Validate settings
if "%s.backends.ObjectPermBackend" % app_label not in settings.AUTHENTICATION_BACKENDS:
    raise ImproperlyConfigured("You have to set '%s.backends.ObjectPermBackend' to AUTHENTICATION_BACKENDS" % app_label)

# Regist templatetags for ObjectPermission
if settings.OBJECT_PERMISSION_BUILTIN_TEMPLATETAG:
    from django.template import add_to_builtins
    add_to_builtins('%s.templatetags.object_permission_tags' % app_label)



def autodiscover():
    """
    Auto-discover INSTALLED_APPS ophandler.py modules and fail silently when
    not present. This forces an import on them to register any handler bits they
    may want.
    """
    import copy
    from django.conf import settings
    from djanto.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's object permission handler module.
        try:
            before_import_registry = copy.copy(manager._registry)
            import_module('%s.ophandler' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            manager._registry = before_import_registry

            # Decide wheter to bubble up this error. If the app just
            # doesn't have an object permission module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'ophandler'):
                raise

if settings.OBJECT_PERMISSION_AUTODISCOVER:
    autodiscover()
