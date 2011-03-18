# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/07
#
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FPAdmin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from models import UserObjectPermission, GroupObjectPermission, AnonymousObjectPermission

#class ObjectPermissionMixin(object):
#    def has_change_permission(self, request, obj=None):
#        opts = self.opts
#        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission(), obj)
#    def has_delete_permission(self, request, obj=None):
#        opts = self.opts
#        return request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission(), obj)
#    
#class UserObjectPermissionInline(GenericTabularInline):
#    model = UserObjectPermission
#    extra = 1
#    raw_id_fields = ['user']
#
#class GroupObjectPermissionInline(GenericTabularInline):
#    model = GroupObjectPermission
#    extra = 1
#    raw_id_fields = ['group']
#
#class AnonymousObjectPermissionInline(GenericTabularInline):
#    model = AnonymousObjectPermission
#    extra = 1
#    max_num = 1
#    can_delete = False
#
#class FlatPageAdmin(ObjectPermissionMixin, FPAdmin):
#    inlines = FPAdmin.inlines + [UserObjectPermissionInline, GroupObjectPermissionInline, AnonymousObjectPermissionInline]
#    
#    def change_view(self, request, *args, **kwargs):
#        try:
#            return super(FlatPageAdmin, self).change_view(request, *args, **kwargs)
#        except PermissionDenied, e:
#            messages.add_message(request, messages.ERROR, u"You don't have the necessary permissions!")
#            return HttpResponseRedirect(reverse('admin:flatpages_flatpage_changelist'))
#
#admin.site.unregister(FlatPage)
#admin.site.register(FlatPage, FlatPageAdmin)

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