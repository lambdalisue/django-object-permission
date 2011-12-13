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
import warnings

from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed

from mediators import ObjectPermissionMediator

__ALL__ = ['ObjectPermissionMediator']

# Set defaut settings
settings.OBJECT_PERMISSION_WARN = getattr(
        settings, 'OBJECT_PERMISSION_WARN', True)
settings.OBJECT_PERMISSION_BUILTIN_TEMPLATETAG = getattr(
        settings, 'OBJECT_PERMISSION_BUILTIN_TEMPLATETAG', True)
settings.OBJECT_PERMISSION_MODIFY_FUNCTION = getattr(
        settings, 'OBJECT_PERMISSION_MODIFY_FUNCTION', 
        'modify_object_permission')
settings.OBJECT_PERMISSION_MODIFY_M2M_FUNCTION = getattr(
        settings, 'OBJECT_PERMISSION_MODIFY_M2M_FUNCTION', 
        'modify_object_permission_m2m')

# Check required settings
if not hasattr(settings, 'AUTHENTICATION_BACKENDS'):
    raise Exception(
            """You must define 'AUTHENTICATION_BACKENDS' in settings.py""")
elif ('object_permission.backends.ObjectPermBackend' not in
        settings.AUTHENTICATION_BACKENDS and settings.OBJECT_PERMISSION_WARN):
    warnings.warn(
            """required ObjectPermBackend is not in AUTHENTICATION_BACKENDS""")

# Regist templatetags for ObjectPermission
if settings.OBJECT_PERMISSION_BUILTIN_TEMPLATETAG:
    from django.template import add_to_builtins
    add_to_builtins('object_permission.templatetags.object_permission_tags')

# Automatically call `modify_permission` of all model
def _post_save_callback(sender, instance, created, **kwargs):
    if hasattr(instance, settings.OBJECT_PERMISSION_MODIFY_FUNCTION):
        fn = getattr(instance, settings.OBJECT_PERMISSION_MODIFY_FUNCTION)
        fn(mediator=ObjectPermissionMediator, created=created)
def _m2m_changed_callback(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ('post_add', 'post_remove') and hasattr(instance, settings.OBJECT_PERMISSION_MODIFY_M2M_FUNCTION):
        fn = getattr(instance, settings.OBJECT_PERMISSION_MODIFY_M2M_FUNCTION)
        fn(mediator=ObjectPermissionMediator, sender=sender, model=model, pk_set=pk_set, removed=action == 'post_remove')
post_save.connect(_post_save_callback)
m2m_changed.connect(_m2m_changed_callback)
