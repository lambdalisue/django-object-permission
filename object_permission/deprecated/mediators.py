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
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import AnonymousUser

from ..models import UserObjectPermission
from ..models import GroupObjectPermission
from ..models import AnonymousObjectPermission

class ObjectPermissionMediator(object):
    """object-permission mediator

    this is used to add/remove permissions of particular user (include
    anonymous) to particular object.

    >>> mediator = ObjectPermissionMediator
    >>> assert callable(getattr(mediator, 'get_permission'))
    >>> assert callable(getattr(mediator, 'contribute'))
    >>> assert callable(getattr(mediator, 'discontribute'))
    >>> assert callable(getattr(mediator, 'manager'))
    >>> assert callable(getattr(mediator, 'editor'))
    >>> assert callable(getattr(mediator, 'viewer'))
    >>> assert callable(getattr(mediator, 'reject'))

    This class is deprecated. Use ObjectPermMediator insted
    """

    @classmethod
    def get_permission(cls, obj, to=None):
        """Get permission for `obj` to `to` with parameter
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated
                        user
        """
        
        ctype = ContentType.objects.get_for_model(obj)
        if isinstance(to, basestring) and to == 'anonymous':
            instance = AnonymousObjectPermission.objects.get_or_create(
                content_type=ctype,
                object_id=obj.pk)[0]
        elif isinstance(to, AnonymousUser):
            instance = AnonymousObjectPermission.objects.get_or_create(
                content_type=ctype,
                object_id=obj.pk)[0]
        elif isinstance(to, Group):
            instance = GroupObjectPermission.objects.get_or_create(
                group=to,
                content_type=ctype,
                object_id=obj.pk)[0]
        else:
            if isinstance(to, basestring):
                to = User.objects.get(username=to)
            instance = UserObjectPermission.objects.get_or_create(
                user=to,
                content_type=ctype,
                object_id=obj.pk)[0]
        return instance
    @classmethod
    def contribute(cls, obj, to=None, permissions=[], clear=False):
        """Contribute permission for `obj` to `to` with parameter
        
        Attribute:
            obj         - tareget object for permission
            to          - User, Group, AnonymousUser to cotribute permission.
                         `None` mean contribute permission to all authenticated
                         user
            permissions - codename list of permission
            append      - `True` to append `permissions`, default is `False`
        
        Notice:
            this method is super method. Use `manager`, `editor`, `viewer` 
            and `reject` for noraml usage.
        """
        ctype = ContentType.objects.get_for_model(obj)
        instance = cls.get_permission(obj, to)
        if clear:
            instance.permissions.clear()
        for perm in permissions:
            try:
                perm = perm.split('.')[-1]
            except IndexError:
                return False
            try:
                permission = Permission.objects.get(
                    content_type=ctype,
                    codename=perm,
                )
            except Permission.DoesNotExist:
                if hasattr(obj, 'object_permission_suffix'):
                    suffix = getattr(obj, 'object_permission_suffix')
                else:
                    # Django default permissions have model name at the end
                    suffix = "_" + str(ctype.model)
                perm = perm + suffix
                permission, created = Permission.objects.get_or_create(
                    content_type=ctype,
                    codename=perm,
                )
            instance.permissions.add(permission)
        instance.save()
        return instance
    @classmethod
    def discontribute(cls, obj, to=None, permissions=[]):
        """Discontribute permission for `obj` to `to` with parameter
        
        Attribute:
            obj         - tareget object for permission
            to          - User, Group, AnonymousUser to cotribute permission.
                         `None` mean contribute permission to all authenticated
                         user
            permissions - codename list of permission
        
        Notice:
            this method is super method. Use `manager`, `editor`, `viewer` 
            and `reject` for noraml usage.
        """
        ctype = ContentType.objects.get_for_model(obj)
        instance = cls.get_permission(obj, to)
        for perm in permissions:
            try:
                perm = perm.split('.')[-1]
            except IndexError:
                return False
            try:
                permission = Permission.objects.get(
                    content_type=ctype,
                    codename=perm,
                )
            except Permission.DoesNotExist:
                if hasattr(obj, 'object_permission_suffix'):
                    suffix = getattr(obj, 'object_permission_suffix')
                else:
                    # Django default permissions have model name at the end
                    suffix = "_" + str(ctype.model)
                perm = perm + suffix
                permission = Permission.objects.get(
                    content_type=ctype,
                    codename=perm,
                )
            instance.permissions.remove(permission)
        instance.save()
        return instance
    @classmethod
    def manager(cls, obj, to, extra_permissions=[]):
        """
        Contribute manager permission (can view, change, delete) for `obj` 
        to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated
                        user
        """
        permissions = ['view', 'change', 'delete'] + list(extra_permissions)
        return cls.contribute(obj, to, permissions, clear=True)
    
    @classmethod
    def editor(cls, obj, to, extra_permissions=[]):
        """
        Contribute editor permission (can view, change. cannot delete) for 
        `obj` to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated
                        user
        """
        permissions = ['view', 'change'] + list(extra_permissions)
        return cls.contribute(obj, to, permissions, clear=True)
    
    @classmethod
    def viewer(cls, obj, to, extra_permissions=[]):
        """
        Contribute viewer permission (can view. cannot change, delete) for 
        `obj` to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated
                        user
        """
        permissions = ['view'] + list(extra_permissions)
        return cls.contribute(obj, to, permissions, clear=True)
    
    @classmethod
    def reject(cls, obj, to, extra_permissions=[]):
        """
        Contribute reject permission (cannot view change, delete) for `obj`
        to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated
                        user
        """
        permissions = [] + list(extra_permissions)
        return cls.contribute(obj, to, permissions, clear=True)
