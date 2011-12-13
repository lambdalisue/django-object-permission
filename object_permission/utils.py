#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
utilities of django-object-permission


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
from django.shortcuts import get_object_or_404

def generic_permission_check(queryset, perm, request, *args, **kwargs):
    """
    Generic permission check

    useful to create custom permission_required decorator. DO NOT create your
    own permission_required while ``permission_required`` decorator is exsits
    at ``object_permission.decorators``
    
    Arguments:
        queryset    - queryset of object
        perm        - permission string
        request     - HttpRequest
        *args       - *args for view function
        **kwargs    - **kwargs for view function
    
    Example:
    >>> from django.http import HttpResponseForbidden
    >>> from django.views.generic import list_detail
    >>> from object_permission.utils import generic_permission_check
    >>> 
    >>> def permission_required(perm, model):
    ...     def wrapper(fn):
    ...         def inner(request, *args, **kwargs):
    ...             # Filtering queryset with `author`
    ...             queryset = model.objects.filter(author=kwargs['author'])
    ...             if not generic_permission_check(queryset, perm, request, *args, **kwargs):
    ...                 return HttpResponseForbidden()
    ...             return fn(request, *args, **kwargs)
    ...         return inner
    ...     return wrapper
    >>> 
    >>> @permission_required('blogs.view_blog', Entry)
    >>> def object_detail(request, *args, **kwargs):
    ...     kwargs['queryset'] = kwargs['queryset'].filter(author__username=kwargs['author'])
    ...     return list_detail.object_list(request, *args, **kwargs)
    
    """
    if queryset is None:
        return request.user.has_perm(perm)
    if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs and 'slug' in kwargs:
        obj = get_object_or_404(queryset,
            publish_at__year=kwargs['year'],
            publish_at__month=kwargs['month'],
            publish_at__day=kwargs['day'],
            title=kwargs['slug'])
    elif 'object_id' in kwargs:
        # For method based generic view
        obj = get_object_or_404(queryset, pk=kwargs['object_id'])
    elif 'pk' in kwargs:
        # For class based generic view
        obj = get_object_or_404(queryset, pk=kwargs['pk'])
    elif 'slug' in kwargs:
        slug_field = kwargs.get('slug_field', 'slug')
        obj = get_object_or_404(queryset, **{slug_field: kwargs['slug']})
    else:
        return request.user.has_perm(perm)
    return request.user.has_perm(perm, obj)
