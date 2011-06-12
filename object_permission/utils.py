# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/07
#
from django.shortcuts import get_object_or_404

#
# Notice:
#    DO NOT USE `generic_permission_check` for normal generic view.
#    there is `permission_check` decorator on `libwaz.contrib.object_permission.decorators`
#    and using `generic_permission_check` approach make no sence.
#    `generic_permission_check` approach only make sence when you need to filtering
#    queryset because otherwise `get` method return multiple objects.
#
#    Example usage:
#    You have a Blog application and you are using `date_based` filtering with `author` field.
#    Then you need to filtering queryset with `author` before hand queryset to permission check
#    
def generic_permission_check(queryset, perm, request, *args, **kwargs):
    u"""
    Generic permission check
    
    Arguments:
        queryset    - queryset of object
        perm        - permission string
        request     - HttpRequest
        *args       - *args for view function
        **kwargs    - **kwargs for view function
    
    Usage:
        from django.http import HttpResponseForbidden
        from django.views.generic import list_detail
        from object_permission.utils import generic_permission_check
        
        def permission_required(perm, model):
            def wrapper(fn):
                def inner(request, *args, **kwargs):
                    # Filtering queryset with `author`
                    queryset = model.objects.filter(author=kwargs['author'])
                    if not generic_permission_check(queryset, perm, request, *args, **kwargs):
                        return HttpResponseForbidden()
                    return fn(request, *args, **kwargs)
                return inner
            return wrapper
        
        @permission_required('blogs.view_blog', Entry)
        def object_detail(request, *args, **kwargs):
            kwargs['queryset'] = kwargs['queryset'].filter(author__username=kwargs['author'])
            return list_detail.object_list(request, *args, **kwargs)
    
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