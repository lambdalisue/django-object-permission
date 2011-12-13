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
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
        
class BaseObjectPermission(models.Model):
    """
    Permission model for perticular object
    """
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'), null=True)
    object_id       = models.PositiveIntegerField(_('object id'), null=True)
    content_object  = generic.GenericForeignKey()
    
    permissions     = models.ManyToManyField(Permission, verbose_name=_('permissions'), null=True)
    
    class Meta:
        abstract    = True
        
class GroupObjectPermission(BaseObjectPermission):
    """
    Object permission model for group
    """
    group   = models.ForeignKey(Group, verbose_name=_('group'))
    
    class Meta:
        ordering            = ('content_type', 'group')
        unique_together     = ('content_type', 'object_id', 'group')
        verbose_name        = _('group object permission')
        verbose_name_plural = _('group object permissions')
        
class AnonymousObjectPermission(BaseObjectPermission):
    """
    Object permission model for anonymous user
    """
    class Meta:
        ordering            = ('content_type',)
        unique_together     = ('content_type', 'object_id')
        verbose_name        = _('anonymous object permission')
        verbose_name_plural = _('anonymous object permissions')

class UserObjectPermission(BaseObjectPermission):
    """
    Object permission model for user
    """
    user    = models.ForeignKey(User, blank=True, null=True, verbose_name=_('user'), help_text=_('`None` for all authenticated user'))
    
    class Meta:
        ordering            = ('content_type', 'user')
        unique_together     = ('content_type', 'object_id', 'user')
        verbose_name        = _('user object permission')
        verbose_name_plural = _('user object permissions')
