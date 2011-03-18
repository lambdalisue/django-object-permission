# -*- coding: utf-8 -*-
#
# Created:        2010/11/07
# Author:        alisue
#
from django.conf import settings
from django.db.models import Q, Model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from models import GroupObjectPermission, AnonymousObjectPermission, UserObjectPermission

import warnings

class ObjectPermBackend(object):
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
            warnings.warn(u"%r doesn't have `%s(self, mediator, created)` function." % (obj.__class__, settings.OBJECT_PERMISSION_MODIFY_FUNCTION))
            
        ct = ContentType.objects.get_for_model(obj)
        
        try:
            perm = perm.split('.')[-1]
        except IndexError:
            return False
        
        # exists check for `perm`
        if not Permission.objects.filter(content_type=ct, codename=perm).exists():
            # Django default permissions have model name at the end.
            _perm = "%s_%s" % (perm, ct.model)
            if not Permission.objects.filter(content_type=ct, codename=_perm).exists():
                permissions = [p.codename for p in Permission.objects.filter(content_type=ct)]
                raise AttributeError("Permission `%s` of `%s` doesn't exists."
                                     " Chose permission from %s or check"
                                     " `http://docs.djangoproject.com/en/dev/topics/auth/#custom-permissions`"
                                     " to create custom permission." % (perm, ct.model, permissions))
            perm = _perm
            
        if user_obj.is_authenticated():
            # try to find from UserObjectPermission first
            qs = UserObjectPermission.objects.filter(content_type=ct, object_id=obj.pk, user=user_obj)
            if not qs.exists():
                # permission for particular user should have priority over permission for all authenticated users
                qs = UserObjectPermission.objects.filter(content_type=ct, object_id=obj.pk, user=None)
            if exists(qs, perm): return True
            qs = GroupObjectPermission.objects.filter(content_type=ct, object_id=obj.pk, group__in= user_obj.groups.all())
            return exists(qs, perm)
        else:
            # try to find from AnonymousObjectPermission
            qs = AnonymousObjectPermission.objects.filter(content_type=ct, object_id=obj.pk)
            return exists(qs, perm)
