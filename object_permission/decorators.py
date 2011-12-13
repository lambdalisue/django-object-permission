#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
decorators for django-object-permission


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
from django.http import HttpResponseForbidden
from django.db.models import Model
from django.contrib.auth.views import redirect_to_login

from utils import generic_permission_check

def permission_required(perm, queryset=None):
    """
    Permission check decorator for generic view
    
    Arguments:
        perm     - permission code same format as Django's permission code
                   when you need ObjectPermission feature only, you can cut
                   off `app_label` and `model` See Usage below.
        queryset - QuerySet or Model object for filtering.
        
    # with old-style generic view
    >>> import django.views.generic.list_detail
    >>> @required_permission('app_label.view_model', Model)
    >>> def model_detail(request, *args, **kwargs):
    ...    return django.views.generic.list_detail.object_detail(
    ...            request, *args, *kwargs)

    # with new-style generic view
    >>> from django.utils.decorators import method_decorator
    >>> import django.views.generic.DetailView
    >>> class ModelDetailView(django.views.generic.DetailView):
    ...     model = model
    ...     @method_decorator(required_permission('app_label.view_model', Model)
    ...     def dispatch(self, *args, **kwargs):
    ...         return super(ModelDetailView, self).dispatch(*args, **kwargs)
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
    warnings.warn(
        "deprecated. use `permission_required` insted", DeprecationWarning)
    return permission_required(perm, queryset)
