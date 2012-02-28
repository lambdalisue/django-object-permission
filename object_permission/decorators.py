#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Decorators of object-permission

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
import inspect

from django.http import HttpRequest
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.views import redirect_to_login

from utils import _get_object_from_list_detail_object_detail
from utils import _get_object_from_date_based_object_detail

def permission_required(perm, queryset=None):
    """
    Permission check decorator for generic view
    
    Arguments:
        perm     - permission code same format as Django's permission code
                   when you need ObjectPermission feature only, you can cut
                   off `app_label` and `model` See Usage below.
        queryset - QuerySet or Model object for filtering.
                   With Classbased generic view, None for using class default
                   queryset if the class have or None for non object permission
                   check.
                   With Functional generic view, None for non object permission
    Note:
        Using Classbased generic view is recommended while you can regulate the
        queryset used with class method in Classbased generic view. Getting object
        from parameters of functional generic view might not work correctly sometime.

    Note:
        This decorator can decorate GenericView class as well. The following code works
        correctly::

            @permission_required('auth.add_user')
            class SomeView(View):
                pass

    Warning:
        DO NOT USE 'django.utils.decorators.method_decorator'. This decorator
        can be used either Classbased/Functional generic view without the 
        method_decorator

    """
    def wrapper(fn):
        def inner(*args, **kwargs):
            args = list(args)
            if 'self' in kwargs:
                self = kwargs.pop('self')
            elif len(args) > 0:
                self = args.pop(0)
            else:
                self = None
            if 'request' in kwargs:
                request = kwargs.pop('request')
            elif len(args) > 0:
                request = args.pop(0)
            else:
                request = None
            if isinstance(self, HttpRequest):
                # functional based generic view
                if request is not None:
                    args.insert(0, request)
                request = self
                self = None
            if self is None:
                if queryset:
                    kwargs['queryset'] = queryset
                    # functional based generic view
                    if 'date_field' in kwargs:
                        # assume that fn is date_based.object_detail
                        obj = _get_object_from_date_based_object_detail(
                                request, *args, **kwargs)
                    else:
                        # assume that fn is list_detail.object_detail
                        obj = _get_object_from_list_detail_object_detail(
                                request, *args, **kwargs)
                else:
                    obj = None
            else:
                # classbased generic view
                if not isinstance(self, CreateView) and isinstance(self, SingleObjectMixin):
                    if not hasattr(self, 'request'):
                        self.request = request
                    self.kwargs = kwargs
                    obj = self.get_object(queryset)
                else:
                    obj = None
            if not request.user.has_perm(perm, obj):
                if request.user.is_authenticated():
                    return HttpResponseForbidden()
                else:
                    return redirect_to_login(request.path)
            if self is None:
                return fn(request, *args, **kwargs)
            else:
                return fn(self, request, *args, **kwargs)
        if inspect.isclass(fn):
            # decorate class
            cls = fn
            dispatch = getattr(cls, 'dispatch')
            dispatch = wrapper(dispatch)
            setattr(cls, 'dispatch', dispatch)
            return cls
        return inner
    return wrapper
