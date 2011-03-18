# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, AnonymousUser, Permission

from models import UserObjectPermission, GroupObjectPermission, AnonymousObjectPermission

class ObjectPermissionMediator(object):
    @classmethod
    def get_permission(cls, obj, to=None):
        u"""
        Get permission for `obj` to `to` with parameter
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated user
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
        u"""
        Contribute permission for `obj` to `to` with parameter
        
        Attribute:
            obj         - tareget object for permission
            to          - User, Group, AnonymousUser to cotribute permission.
                         `None` mean contribute permission to all authenticated user
            permissions - codename list of permission
            append      - `True` to append `permissions`, default is `False`
        
        Notice:
            this method is super method. Use `manager`, `editor`, `viewer` and `reject`
            for noraml usage.
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
                # Django default permissions have model name at the end
                perm = "%s_%s" % (perm, ctype.model)
                permission = Permission.objects.get(
                    content_type=ctype,
                    codename=perm,
                )
            instance.permissions.add(permission)
        instance.save()
        return instance
    @classmethod
    def discontribute(cls, obj, to=None, permissions=[]):
        u"""
        Discontribute permission for `obj` to `to` with parameter
        
        Attribute:
            obj         - tareget object for permission
            to          - User, Group, AnonymousUser to cotribute permission.
                         `None` mean contribute permission to all authenticated user
            permissions - codename list of permission
            append      - `True` to append `permissions`, default is `False`
        
        Notice:
            this method is super method. Use `manager`, `editor`, `viewer` and `reject`
            for noraml usage.
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
                # Django default permissions have model name at the end
                perm = "%s_%s" % (perm, ctype.model)
                permission = Permission.objects.get(
                    content_type=ctype,
                    codename=perm,
                )
            instance.permissions.remove(permission)
        instance.save()
        return instance
    @classmethod
    def manager(cls, obj, to, extra_permissions=[]):
        u"""
        Contribute manager permission (can view, change, delete) for `obj` to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` can_view   - `view` permissionOld permission
            can_change - `change` permission
            can_delete - `delete` permissionmean contribute permission to all authenticated user
        """
        return cls.contribute(obj, to, ['view', 'change', 'delete']+list(extra_permissions), clear=True)
    
    @classmethod
    def editor(cls, obj, to, extra_permissions=[]):
        u"""
        Contribute editor permission (can view, change. cannot delete) for `obj` to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated user
        """
        return cls.contribute(obj, to, ['view', 'change']+list(extra_permissions), clear=True)
    
    @classmethod
    def viewer(cls, obj, to, extra_permissions=[]):
        u"""
        Contribute viewer permission (can view. cannot change, delete) for `obj` to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated user
        """
        return cls.contribute(obj, to, ['view']+list(extra_permissions), clear=True)
    
    @classmethod
    def reject(cls, obj, to, extra_permissions=[]):
        u"""
        Contribute reject permission (cannot view change, delete) for `obj` to `to`
        
        Attribute:
            obj        - tareget object for permission
            to         - User, Group, AnonymousUser to cotribute permission.
                        `None` mean contribute permission to all authenticated user
        """
        return cls.contribute(obj, to, []+list(extra_permissions), clear=True)