#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
auth backend to use django-object-permission

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
import warnings

from django.conf import settings
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from models import UserObjectPermission
from models import GroupObjectPermission
from models import AnonymousObjectPermission


class ObjectPermBackend(object):
    """Authentication backend for object-permission"""
    supports_object_permissions = True
    supports_anonymous_user     = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        def exists(qs, perm):
            return qs.filter(permissions__codename=perm).distinct().exists()
        
        if obj is None or not isinstance(obj, Model):
            return False
        
        if not hasattr(obj, settings.OBJECT_PERMISSION_MODIFY_FUNCTION):
            warnings.warn(
                    """%r doesn't have `%s` function.""" % (
                        obj.__class__, 
                        settings.OBJECT_PERMISSION_MODIFY_FUNCTION
                    ))
            
        ct = ContentType.objects.get_for_model(obj)
        
        try:
            perm = perm.split('.')[-1]
        except IndexError:
            return False
        
        # exists check for `perm`
        if not Permission.objects.filter(
                content_type=ct, codename=perm).exists():
            # To enable custom suffix
            if hasattr(obj, 'object_permission_suffix'):
                suffix = getattr(obj, 'object_permission_suffix')
            else:
                # Django default permissions have model name at the end.
                suffix = "_" + str(ct.model)
            _perm = perm + suffix
            if not Permission.objects.filter(
                    content_type=ct, codename=_perm).exists():
                permissions = [p.codename for p in 
                        Permission.objects.filter(content_type=ct)]
                raise AttributeError(
                    "Permission `%s` of `%s` doesn't exists."
                    " Chose permission from %s or check"
                    " `http://docs.djangoproject.com/en/dev/topics/auth/#custom-permissions`"
                    " to create custom permission." % (perm, ct.model, permissions))
            perm = _perm
            
        if user_obj.is_authenticated():
            # try to find from UserObjectPermission first
            qs = UserObjectPermission.objects.filter(
                    content_type=ct, object_id=obj.pk, user=user_obj)
            if not qs.exists():
                # permission for particular user should have priority over 
                # permission for all authenticated users
                qs = UserObjectPermission.objects.filter(
                        content_type=ct, object_id=obj.pk, user=None)
            if exists(qs, perm): return True
            qs = GroupObjectPermission.objects.filter(
                    content_type=ct, object_id=obj.pk, 
                    group__in= user_obj.groups.all())
            return exists(qs, perm)
        else:
            # try to find from AnonymousObjectPermission
            qs = AnonymousObjectPermission.objects.filter(
                    content_type=ct, object_id=obj.pk)
            return exists(qs, perm)
