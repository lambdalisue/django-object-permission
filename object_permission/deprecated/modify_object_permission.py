#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed

from .. import set_default
from mediators import ObjectPermissionMediator

set_default('OBJECT_PERMISSION_MODIFY_FUNCTION', 'modify_object_permission')
set_default('OBJECT_PERMISSION_MODIFY_M2M_FUNCTION', 'modify_object_permission_m2m')

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
