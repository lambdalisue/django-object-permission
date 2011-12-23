#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Authentication Backend for 'django.contrib.auth' app

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
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType

from models import UserObjectPermission
from models import GroupObjectPermission
from models import AnonymousObjectPermission

from utils import get_perm_codename

class ObjectPermBackend(object):
    """Authentication backend for object-permission"""
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        """This backend is only for checking permission"""
        return None

    def _has_user_object_permission(cls, user_obj, perm_codename, obj):
        """check permission of obj for user from UserObjectPermission"""
        if user_obj and not user_obj.is_authenticated():
            return False
        ct = ContentType.objects.get_for_model(obj)
        qs = UserObjectPermission.objects.filter(
                content_type=ct,
                object_id=obj.pk,
                user=user_obj)
        qs = qs.filter(permissions__codename=perm_codename).distinct()
        return qs.exists()

    def _has_group_object_permission(cls, user_obj, perm_codename, obj):
        """check permission of obj for user from GroupObjectPermission"""
        if not user_obj.is_authenticated():
            return False
        ct = ContentType.objects.get_for_model(obj)
        qs = GroupObjectPermission.objects.filter(
                content_type=ct,
                object_id=obj.pk,
                group__in=user_obj.groups.all())
        qs = qs.filter(permissions__codename=perm_codename).distinct()
        return qs.exists()

    def _has_anonymous_object_permission(cls, user_obj, perm_codename, obj):
        """check permission of obj for anonymous from AnonymousObjectPermission"""
        if user_obj.is_authenticated():
            return False
        ct = ContentType.objects.get_for_model(obj)
        qs = AnonymousObjectPermission.objects.filter(
                content_type=ct,
                object_id=obj.pk)
        qs = qs.filter(permissions__codename=perm_codename).distinct()
        return qs.exists()

    def has_perm(self, user_obj, perm, obj=None):
        """check permission of obj for user_obj"""
        if obj is None or not isinstance(obj, Model):
            # This is object permission backend so don't touch if obj is None
            return False
        
        perm_codename = get_perm_codename(perm)
            
        if user_obj.is_authenticated():
            # check user_obj specific permissions
            if self._has_user_object_permission(user_obj, perm_codename, obj):
                return True
            # check authenticated user permissions
            elif self._has_user_object_permission(None, perm_codename, obj):
                return True
            # check groups user_obj belong specific permissions
            elif self._has_group_object_permission(user_obj, perm_codename, obj):
                return True
        # check anonymous user specific permissions
        elif self._has_anonymous_object_permission(user_obj, perm_codename, obj):
            return True
        return False
