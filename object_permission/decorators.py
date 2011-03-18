# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/07
#
from django.http import HttpResponseForbidden
from django.db.models import Model
from django.contrib.auth.views import redirect_to_login

from utils import generic_permission_check

def permission_required(perm, queryset=None):
    u"""
    Permission check decorator for generic view
    
    Arguments:
        perm     - permission code same format as Django's permission code
                   when you need ObjectPermission feature only, you can cut
                   off `app_label` and `model` See Usage below.
        queryset - QuerySet or Model object for filtering.
        
    Usage:
        @required_permission('app_label.view_model', Model)
        def object_detail(request, *args, **kwargs):
            ...
        
        If you need `ObjectPermission` only, you can cut of app_label and model like below
        
        @required_permission('view', Model)
        def object_detial(request, *args, **kwargs):
            ...
        
    """
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            if queryset and issubclass(queryset, Model):
                qs = queryset.objects.all()
            else:
                qs = queryset
            if not generic_permission_check(qs, perm, request, *args, **kwargs):
                if request.user.is_authenticated():
                    return HttpResponseForbidden()
                else:
                    return redirect_to_login(request.path)
            return fn(request, *args, **kwargs)
        return inner
    return wrapper

# Deprecation Function
import warnings
def permission_check(perm, queryset=None):
    warnings.warn("`permission_check` function is deprecationed. Use `permission_required` insted", DeprecationWarning)
    return permission_required(perm, queryset)
