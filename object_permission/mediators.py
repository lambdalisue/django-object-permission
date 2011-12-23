#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
object-permission mediator module

mediator is to use add/remove permissions to particular object


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
from django.db.models import Model
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType

from models import UserObjectPermission
from models import GroupObjectPermission
from models import AnonymousObjectPermission
from utils import get_perm_codename
from utils import get_perm_codename_with_suffix

class ObjectPermMediatorBase(object):
    """Base Mediator for object-permission"""

    def __init__(self, obj):
        """constructor for ObjectPermMediator

        Attribute:
            obj - a target model instance of object permission
        """
        if not isinstance(obj, Model):
            raise AttributeError("'%s' is not an instance of model" % obj)
        self._obj = obj
        self._ct = ContentType.objects.get_for_model(obj)

    def _get_or_create_permission(self, perm):
        """get or create django permission instance"""
        perm_codename = get_perm_codename(perm)
        try:
            # try to find permissin without suffix
            permission = Permission.objects.get(
                    content_type=self._ct,
                    codename=perm_codename)
        except Permission.DoesNotExist:
            # try to find/create permission with suffix
            perm_codename = get_perm_codename_with_suffix(perm, self._obj)
            permission = Permission.objects.get_or_create(
                    content_type=self._ct,
                    codename=perm_codename)[0]
        return permission

    def _get_object_permission_cls(self, instance):
        """get object permission cls suite for instance"""
        ANONYMOUS = 'anonymous'
        if isinstance(instance, basestring) and instance == ANONYMOUS:
            return AnonymousObjectPermission, {}
        elif isinstance(instance, AnonymousUser):
            return AnonymousObjectPermission, {}
        elif isinstance(instance, Group):
            return GroupObjectPermission, {'group': instance}
        elif instance is None or isinstance(instance, User) or isinstance(instance, basestring):
            if isinstance(instance, basestring):
                # Search from username
                try:
                    instance = User.objects.get(username=instance)
                except User.DoesNotExist:
                    raise AttributeError("Unknown parameter '%s' is passed, you may mean '%s'?" % (instance, ANONYMOUS))
            return UserObjectPermission, {'user': instance}
        raise AttributeError("Unknown parameter '%s' is passed" % instance)

    def _get_or_create_object_permission(self, instance):
        """get or create object permission suite for instance"""
        model, kwargs = self._get_object_permission_cls(instance)
        return model.objects.get_or_create_object_permission(self._obj, **kwargs)[0]

    def reset(self):
        """reset all permissions of obj"""
        AnonymousObjectPermission.objects.get_for_model(self._obj).remove()
        GroupObjectPermission.objects.get_for_model(self._obj).remove()
        UserObjectPermission.objects.get_for_model(self._obj).remove()

    def clear(self, instance_or_iterable):
        """clear all object permissions of obj for instance(s)"""
        if not hasattr(instance_or_iterable, '__iter__'):
            instance_or_iterable = [instance_or_iterable]
        for instance in instance_or_iterable:
            object_permission = self._get_or_create_object_permission(instance)
            object_permission.permissions.clear()

    def contribute(self, instance_or_iterable, permissions=[]):
        """contribute permissions of obj to instance(s)

        instances can be an instance of User, Group, AnonymousUser or 'anonymous'
        for AnonymousUser shortcut and None for All authenticated user.

        Attribute:
            instance_or_iterable - User, Group, AnonymousUser to cotribute permission.
                                   'anonymous' for anonymous user and None for all
                                   authenticated users
            permissions          - codename list of permission
        """
        if not hasattr(instance_or_iterable, '__iter__'):
            instance_or_iterable = [instance_or_iterable]
        for instance in instance_or_iterable:
            object_permission = self._get_or_create_object_permission(instance)
            for perm in permissions:
                permission = self._get_or_create_permission(perm)
                object_permission.permissions.add(permission)

    def discontribute(self, instance_or_iterable, permissions=[]):
        """discontribute permissions of obj to instance(s)

        instances can be an instance of User, Group, AnonymousUser or 'anonymous'
        for AnonymousUser shortcut and None for All authenticated user.

        Attribute:
            instance_or_iterable - User, Group, AnonymousUser to cotribute permission.
                                   'anonymous' for anonymous user and None for all
                                   authenticated users
            permissions          - codename list of permission
        """
        if not hasattr(instance_or_iterable, '__iter__'):
            instance_or_iterable = [instance_or_iterable]
        for instance in instance_or_iterable:
            object_permission = self._get_or_create_object_permission(instance)
            for perm in permissions:
                permission = self._get_or_create_permission(perm)
                object_permission.permissions.remove(permission)

class ObjectPermMediator(ObjectPermMediatorBase):
    """Mediator class for object permission"""
    def _contribute(self, instance_or_iterable, permissions, extra_permissions):
        if isinstance(extra_permissions, (list, tuple)):
            permissions += list(extra_permissions)
        self.clear(instance_or_iterable)
        self.contribute(instance_or_iterable, permissions)

    def reject(self, instance_or_iterable, extra_permissions=[]):
        """reject all management permission (view, change, delete)"""
        permissions = []
        self._contribute(instance_or_iterable, permissions, extra_permissions)
    def viewer(self, instance_or_iterable, extra_permissions=[]):
        """can view"""
        permissions = ['view']
        self._contribute(instance_or_iterable, permissions, extra_permissions)
    def ediinstance_or_iterabler(self, instance_or_iterable, extra_permissions=[]):
        """can view and change"""
        permissions = ['view', 'change']
        self._contribute(instance_or_iterable, permissions, extra_permissions)
    def manager(self, instance_or_iterable, extra_permissions=[]):
        """can view, change and delete"""
        permissions = ['view', 'change', 'delete']
        self._contribute(instance_or_iterable, permissions, extra_permissions)
