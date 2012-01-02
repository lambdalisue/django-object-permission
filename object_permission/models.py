#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
models of django-object-permission


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
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
        
class BaseObjectPermissionManager(models.Manager):
    def get_for_model(self, obj):
        """get all object permissions for obj"""
        ct = ContentType.objects.get_for_model(obj)
        pk = obj.pk
        lookup_kwargs = {
                'content_type': ct,
                'object_id': pk,
            }
        return self.filter(**lookup_kwargs)
    def _get_filter_kwargs(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        pk = obj.pk
        kwargs = {
                'content_type': ct,
                'object_id': pk
            }
        return kwargs
    def create_object_permission(self, obj, **kwargs):
        """create object permission"""
        kwargs = self._get_filter_kwargs(obj, **kwargs)
        return self.create(**kwargs)
    def get_or_create_object_permission(self, obj, **kwargs):
        """get or create object permission"""
        kwargs = self._get_filter_kwargs(obj, **kwargs)
        return self.get_or_create(**kwargs)

class BaseObjectPermission(models.Model):
    """
    Permission model for perticular object
    """
    content_type    = models.ForeignKey(
        ContentType, verbose_name=_('content type'), null=True)
    object_id       = models.PositiveIntegerField(_('object id'), null=True)
    content_object  = generic.GenericForeignKey()
    
    permissions     = models.ManyToManyField(
        Permission, verbose_name=_('permissions'), null=True)
    
    class Meta:
        abstract    = True
        
class GroupObjectPermissionManager(BaseObjectPermissionManager):
    def _get_filter_kwargs(self, obj, group):
        kwargs = super(GroupObjectPermissionManager, self)._get_filter_kwargs(obj)
        kwargs['group'] = group
        return kwargs
    def create_object_permission(self, obj, group):
        """create object permission"""
        return super(GroupObjectPermissionManager, self).create_object_permission(obj, group=group)
    def get_or_create_object_permission(self, obj, group):
        """get or create object permission"""
        return super(GroupObjectPermissionManager, self).get_or_create_object_permission(obj, group=group)

class GroupObjectPermission(BaseObjectPermission):
    """
    Object permission model for group
    """
    group   = models.ForeignKey(Group, verbose_name=_('group'))
    objects = GroupObjectPermissionManager()
    
    class Meta:
        ordering            = ('content_type', 'group')
        unique_together     = ('content_type', 'object_id', 'group')
        verbose_name        = _('group object permission')
        verbose_name_plural = _('group object permissions')

    def __unicode__(self):
        return u"GroupObjectPermission of '%s' for '%s'" % (self.content_object, self.group)
        
class AnonymousObjectPermissionManager(BaseObjectPermissionManager):
    def create_object_permission(self, obj):
        """create object permission"""
        return super(AnonymousObjectPermissionManager, self).create_object_permission(obj)
    def get_or_create_object_permission(self, obj):
        """get or create object permission"""
        return super(AnonymousObjectPermissionManager, self).get_or_create_object_permission(obj)

class AnonymousObjectPermission(BaseObjectPermission):
    """
    Object permission model for anonymous user
    """
    objects = AnonymousObjectPermissionManager()

    class Meta:
        ordering            = ('content_type',)
        unique_together     = ('content_type', 'object_id')
        verbose_name        = _('anonymous object permission')
        verbose_name_plural = _('anonymous object permissions')

    def __unicode__(self):
        return u"AnonymousObjectPermission of '%s'" % self.content_object

class UserObjectPermissionManager(BaseObjectPermissionManager):
    def _get_filter_kwargs(self, obj, user):
        kwargs = super(UserObjectPermissionManager, self)._get_filter_kwargs(obj)
        kwargs['user'] = user
        return kwargs
    def create_object_permission(self, obj, user):
        """create object permission"""
        return super(UserObjectPermissionManager, self).create_object_permission(obj, user=user)
    def get_or_create_object_permission(self, obj, user):
        """get or create object permission"""
        return super(UserObjectPermissionManager, self).get_or_create_object_permission(obj, user=user)

class UserObjectPermission(BaseObjectPermission):
    """
    Object permission model for user
    """
    user    = models.ForeignKey(
        User, blank=True, null=True, 
        verbose_name=_('user'), 
        help_text=_('`None` for all authenticated user'))
    objects = UserObjectPermissionManager()
    
    class Meta:
        ordering            = ('content_type', 'user')
        unique_together     = ('content_type', 'object_id', 'user')
        verbose_name        = _('user object permission')
        verbose_name_plural = _('user object permissions')

    def __unicode__(self):
        return u"UserObjectPermission of '%s' for '%s'" % (self.content_object, self.user)
