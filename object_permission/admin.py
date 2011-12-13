#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
admin-site for django-object-permission


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
from django.contrib import admin
from models import UserObjectPermission, GroupObjectPermission, AnonymousObjectPermission

class ObjectPermissionAdmin(admin.ModelAdmin):
    def _get_permissions(self, obj):
        permissions = []
        for permission in obj.permissions.all():
            permissions.append(permission.codename)
        if not permissions:
            return "-"
        return "<br />".join(permissions)
    _get_permissions.allow_tags = True
    _get_permissions.short_description = "Permissions"
class UserObjectPermissionAdmin(ObjectPermissionAdmin):
    list_display    = ('content_type', 'content_object', 'user', '_get_permissions')
    list_filter     = ('content_type', 'user', 'permissions')
    search_fields   = ('permissions', 'user',)
class GroupObjectPermissionAdmin(ObjectPermissionAdmin):
    list_display    = ('content_type', 'content_object', 'group', '_get_permissions')
    list_filter     = ('content_type', 'group', 'permissions')
    search_fields   = ('permissions', 'group',)
class AnonymousObjectPermissionAdmin(ObjectPermissionAdmin):
    list_display    = ('content_type', 'content_object', '_get_permissions')
    list_filter     = ('content_type', 'permissions')
    search_fields   = ('permissions',)
admin.site.register(UserObjectPermission, UserObjectPermissionAdmin)
admin.site.register(GroupObjectPermission, GroupObjectPermissionAdmin)
admin.site.register(AnonymousObjectPermission, AnonymousObjectPermissionAdmin)
