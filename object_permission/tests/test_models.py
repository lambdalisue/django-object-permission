#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of models of object-permission


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
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes.models import ContentType

from base import TestCase
from ..models import GroupObjectPermissin

class GroupObjectPermissionTest(TestCase):
    fixtures = ['test.yaml']

    def test_000_creation(self):
        """object_permission.GroupObjectPermission: creation works correctly"""
        ct = ContentType.objects.get(pk=1)
        group = Group.objects.get(pk=1)
        instance = GroupObjectPermission.objects.create(
                content_type=ct,
                object_id=1,
                



