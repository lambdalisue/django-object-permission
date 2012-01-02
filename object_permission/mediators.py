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
from django.core.exceptions import ObjectDoesNotExist
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

def get_iterable_instances(instance_or_iterable):
    """get iterable instances from instance_or_iterable"""
    from django.db import models
    if isinstance(instance_or_iterable, models.Manager):
        instance_or_iterable = instance_or_iterable.iterator()
    elif not hasattr(instance_or_iterable, '__iter__'):
        instance_or_iterable = [instance_or_iterable]
    return instance_or_iterable

class ObjectPermMediatorBase(object):
    """Base Mediator for object-permission"""

    def __init__(self, instance):
        """constructor for ObjectPermMediator

        Attribute:
            instance - a target model instance of object permission
        """
        if not isinstance(instance, Model):
            raise AttributeError("'%s' is not an instance of model" % instance)
        self.instance = instance
        self._ct = ContentType.objects.get_for_model(instance)

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
            perm_codename = get_perm_codename_with_suffix(perm, self.instance)
            permission = Permission.objects.get_or_create(
                    content_type=self._ct,
                    codename=perm_codename)[0]
        return permission

    def _get_object_permission_cls(self, target):
        """get object permission cls suite for target"""
        ANONYMOUS = 'anonymous'
        if isinstance(target, basestring) and target == ANONYMOUS:
            return AnonymousObjectPermission, {}
        elif isinstance(target, AnonymousUser):
            return AnonymousObjectPermission, {}
        elif isinstance(target, Group):
            return GroupObjectPermission, {'group': target}
        elif target is None or isinstance(target, User) or isinstance(target, basestring):
            if isinstance(target, basestring):
                # Search from username
                try:
                    target = User.objects.get(username=target)
                except User.DoesNotExist:
                    raise AttributeError("Unknown parameter '%s' is passed, you may mean '%s'?" % (target, ANONYMOUS))
            return UserObjectPermission, {'user': target}
        raise AttributeError("Unknown parameter '%s' is passed" % target)

    def _get_or_create_object_permission(self, target):
        """get or create object permission suite for instance"""
        model, kwargs = self._get_object_permission_cls(target)
        return model.objects.get_or_create_object_permission(self.instance, **kwargs)[0]

    def reset(self):
        """reset all permissions of obj"""
        AnonymousObjectPermission.objects.get_for_model(self.instance).delete()
        GroupObjectPermission.objects.get_for_model(self.instance).delete()
        UserObjectPermission.objects.get_for_model(self.instance).delete()

    def clear(self, instance_or_iterable):
        """clear all object permissions of obj for instance(s)"""
        instance_or_iterable = get_iterable_instances(instance_or_iterable)
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
        instance_or_iterable = get_iterable_instances(instance_or_iterable)
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
        instance_or_iterable = get_iterable_instances(instance_or_iterable)
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
    def editor(self, instance_or_iterable, extra_permissions=[]):
        """can view and change"""
        permissions = ['view', 'change']
        self._contribute(instance_or_iterable, permissions, extra_permissions)
    def manager(self, instance_or_iterable, extra_permissions=[]):
        """can view, change and delete"""
        permissions = ['view', 'change', 'delete']
        self._contribute(instance_or_iterable, permissions, extra_permissions)
