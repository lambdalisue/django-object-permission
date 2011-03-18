# -*- coding: utf-8 -*-
#
# Created:        2010/11/07
# Author:        alisue
#
# ref: http://djangoadvent.com/1.2/object-permissions/
#
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
        
class ObjectPermission(models.Model):
    u"""
    Permission model for perticular object
    """
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'), null=True)
    object_id       = models.PositiveIntegerField(_('object id'), null=True)
    content_object  = generic.GenericForeignKey()
    
    permissions     = models.ManyToManyField(Permission, verbose_name=_('permissions'), null=True)
    
    class Meta:
        abstract    = True
        
class GroupObjectPermission(ObjectPermission):
    u"""
    Object permission model for group
    """
    group   = models.ForeignKey(Group, verbose_name=_('group'))
    
    class Meta:
        ordering            = ('content_type', 'group')
        unique_together     = ('content_type', 'object_id', 'group')
        verbose_name        = _('group object permission')
        verbose_name_plural = _('group object permissions')
        
class AnonymousObjectPermission(ObjectPermission):
    u"""
    Object permission model for anonymous user
    """
    class Meta:
        ordering            = ('content_type',)
        unique_together     = ('content_type', 'object_id')
        verbose_name        = _('anonymous object permission')
        verbose_name_plural = _('anonymous object permissions')

class UserObjectPermission(ObjectPermission):
    u"""
    Object permission model for user
    """
    user    = models.ForeignKey(User, blank=True, null=True, verbose_name=_('user'), help_text=_('`None` for all authenticated user'))
    
    class Meta:
        ordering            = ('content_type', 'user')
        unique_together     = ('content_type', 'object_id', 'user')
        verbose_name        = _('user object permission')
        verbose_name_plural = _('user object permissions')