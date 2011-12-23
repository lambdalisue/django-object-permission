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
from ..utils import _get_object_from_date_based_object_detail
from ..utils import _get_object_from_list_detail_object_detail

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
    
    Note:
        This function is deprecated because it is for Functional generic view. 
        Getting object from parameters of functional generic view does not work
        sometimes because of the limitation.
    """
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
    return request.user.has_perm(perm, obj)
