# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/07
#
from django.conf import settings

settings.OBJECT_PERMISSION_MODIFY_FUNCTION = getattr(settings, 'OBJECT_PERMISSION_MODIFY_FUNCTION', 'modify_object_permission')
settings.OBJECT_PERMISSION_MODIFY_M2M_FUNCTION = getattr(settings, 'OBJECT_PERMISSION_MODIFY_M2M_FUNCTION', 'modify_object_permission_m2m')
from mediators import ObjectPermissionMediator

# Regist templatetags for ObjectPermission
from django.template import add_to_builtins
add_to_builtins('object_permission.templatetags.object_permission_tags')

# Automatically call `modify_permission` of all model
from django.db.models.signals import post_save, m2m_changed
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