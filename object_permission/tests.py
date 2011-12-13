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
from django.conf import settings
from django.test import TestCase as _TestCase
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User, Group, AnonymousUser

from mediators import ObjectPermissionMediator

from django.conf import settings
from django.core.management import call_command
from django.db.models import loading

class TestCase(_TestCase):
    apps = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.flatpages',
        'object_permission',
    )

    def _pre_setup(self):
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        for app in self.apps:
            settings.INSTALLED_APPS.append(app)
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0)
        # Call the original method that does the fixtures etc.
        super(TestCase, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(TestCase, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False

class UserObjectPermBackendTest(TestCase):
    def setUp(self):
        super(UserObjectPermBackendTest, self).setUp()
        self.james = User.objects.create_user('james', 'james@example.com', 'james')
        self.emily = User.objects.create_user('emily', 'emily@example.com', 'emily')
        self.peter = User.objects.create_user('peter', 'emily@example.com', 'peter')
        self.fread = AnonymousUser()
        self.page = FlatPage.objects.create(url='/test/', title='test', content='James can see this content but emily.')
        # for checking permission for all authenticated user
        ObjectPermissionMediator.viewer(self.page, None)
        # for checking permission for particular user
        ObjectPermissionMediator.manager(self.page, self.james)
        ObjectPermissionMediator.editor(self.page, self.emily)
        # for checking overwrite permission for particular user
        ObjectPermissionMediator.reject(self.page, self.peter)
        
    def test_permission(self):
        # James has view, change, delete
        self.assertTrue(self.james.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(self.james.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(self.james.has_perm('flatpages.delete_flatpage', self.page))
        # Emliy has view, change but delete
        self.assertTrue(self.emily.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(self.emily.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.emily.has_perm('flatpages.delete_flatpage', self.page))
        # Peter never has any permission
        self.assertTrue(not self.peter.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(not self.peter.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.peter.has_perm('flatpages.delete_flatpage', self.page))
        # Fread never has any permission because he is not authenticated
        self.assertTrue(not self.fread.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(not self.fread.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.fread.has_perm('flatpages.delete_flatpage', self.page))

class GroupObjectPermBackendTest(TestCase):
    def setUp(self):
        super(GroupObjectPermBackendTest, self).setUp()
        self.james = User.objects.create_user('james', 'james@example.com', 'james')
        self.emily = User.objects.create_user('emily', 'emily@example.com', 'emily')
        self.peter = User.objects.create_user('peter', 'emily@example.com', 'peter')
        self.fread = AnonymousUser()
        self.manager = Group.objects.create(name='manager')
        self.editor = Group.objects.create(name='editor')
        self.james.groups.add(self.manager)
        self.james.groups.add(self.editor)
        self.emily.groups.add(self.editor)
        self.page = FlatPage.objects.create(url='/test/', title='test', content='James can see this content but emily.')
        # for checking permission for all authenticated user
        ObjectPermissionMediator.viewer(self.page, None)
        # for checking permission for particular group
        ObjectPermissionMediator.manager(self.page, self.manager)
        ObjectPermissionMediator.editor(self.page, self.editor)
        
    def test_permission(self):
        # James has view, change, delete
        self.assertTrue(self.james.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(self.james.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(self.james.has_perm('flatpages.delete_flatpage', self.page))
        # Emliy has view, change but delete
        self.assertTrue(self.emily.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(self.emily.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.emily.has_perm('flatpages.delete_flatpage', self.page))
        # Peter has view
        self.assertTrue(self.peter.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(not self.peter.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.peter.has_perm('flatpages.delete_flatpage', self.page))
        # Fread never has any permission because he is not authenticated
        self.assertTrue(not self.fread.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(not self.fread.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.fread.has_perm('flatpages.delete_flatpage', self.page))

class AnonymousObjectPermBackendTest(TestCase):
    def setUp(self):
        super(AnonymousObjectPermBackendTest, self).setUp()
        self.james = User.objects.create_user('james', 'james@example.com', 'james')
        self.fread = AnonymousUser()
        self.page = FlatPage.objects.create(url='/test/', title='test', content='James can see this content but emily.')
        # for checking permission for all authenticated user
        ObjectPermissionMediator.viewer(self.page, None)
        # for checking permission for anonymous user
        ObjectPermissionMediator.manager(self.page, 'anonymous')
        
    def test_permission(self):
        # James has view
        self.assertTrue(self.james.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(not self.james.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(not self.james.has_perm('flatpages.delete_flatpage', self.page))
        # Fread has view, change, delete because he is anonymous user
        self.assertTrue(self.fread.has_perm('flatpages.view_flatpage', self.page))
        self.assertTrue(self.fread.has_perm('flatpages.change_flatpage', self.page))
        self.assertTrue(self.fread.has_perm('flatpages.delete_flatpage', self.page))
