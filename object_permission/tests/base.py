#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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
from app_test import AppTestCase

class ObjectPermissionTestCaseBase(AppTestCase):
    installed_apps = [
            'author',
            'object_permission.tests.app',
        ]
    middleware_classes = [
            'author.middlewares.AuthorDefaultBackendMiddleware',
        ]

    def _pre_setup(self):
        super(ObjectPermissionTestCaseBase, self)._pre_setup()
        from .. import autodiscover
        autodiscover()
