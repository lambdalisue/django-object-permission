# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/07
#
from django.test import TestCase
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, AnonymousUser

from mediators import ObjectPermissionMediator

class UserObjectPermBackendTest(TestCase):
    def setUp(self):
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