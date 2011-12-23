#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
utilities of object-permission


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
import time
import datetime

from django.http import Http404
from django.db.models.fields import DateTimeField
from django.shortcuts import get_object_or_404

def get_perm_codename(perm):
    """get permission codename from django's standard permission format"""
    # Note:
    #   'app_label.permission_codename' is a standard permission format

    try:
        app, perm = perm.split('.', 1)
    except ValueError:
        # Non standard permission
        pass
    return perm

def get_perm_codename_with_suffix(perm, obj):
    """get permission codename suffix"""
    perm_codename = get_perm_codename(perm)
    if hasattr(obj, 'object_permission_suffix'):
        suffix = getattr(obj, 'object_permission_suffix')
    else:
        suffix = "_%s" % obj.__class__.__name__.lower()
    if perm_codename.endswith(suffix):
        return perm_codename
    return perm_codename + suffix
    
def _get_object_from_list_detail_object_detail(
        request, queryset, object_id=None, slug=None, 
        slug_field='slug', *args, **kwargs):
    """get object from parameters passed to list_detail.object_detail"""
    if object_id:
        obj = get_object_or_404(queryset, pk=object_id)
    elif slug and slug_field:
        obj = get_object_or_404(queryset, **{slug_field: slug})
    else:
        raise AttributeError(
                "Generic detail view must be called with either an "
                "object_id or a slug/slug_field.")
    return obj

def _get_object_from_date_based_object_detail(
        request, year, month, day, queryset, date_field,
        month_format='%b', day_format='%d', object_id=None,
        slug=None, slug_field='slug', **kwargs):
    """get object from parameters passed to date_based.object_detail"""
    from django.utils import timezone
    try:
        tt = time.strptime('%s-%s-%s' % (year, month, day), 
                            '%s-%s-%s' % ('%Y', month_format, day_format))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    model = queryset.model
    now = timezone.now()

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {
                '%s__range' % date_field: (
                    datetime.datetime.combine(date, datetime.time.min),
                    datetime.datetime.combine(date, datetime.time.max)
                )}
    else:
        lookup_kwargs = {date_field: date}

    if date >= now.date() and not kwargs.get('allow_future', False):
        lookup_kwargs['%s__lte' % date_field] = now
    if object_id:
        lookup_kwargs['pk'] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError(
                "Generic detail view must be called with either an "
                "object_id or a slug/slug_field.")
    return get_object_or_404(queryset, **lookup_kwargs)
