#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of ...


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
from django.contrib.auth.models import AnonymousUser

from app_testcase import AppTestCase

class ArticleTestCase(AppTestCase):
    fixtures = ['test.yaml']
    installed_apps = [
            'author',
            'object_permission.tests.testapp',
        ]
    middleware_classes = [
            'author.middlewares.AuthorDefaultBackendMiddleware',
        ]

    def _pre_setup(self):
        super(ArticleTestCase, self)._pre_setup()
        from .. import autodiscover
        autodiscover()

    def setUp(self):
        from testapp.models import Article
        self.foo = User.objects.get(username='foo')
        self.foofoo = User.objects.get(username='foofoo')
        self.foofoofoo = User.objects.get(username='foofoofoo')
        self.bar = User.objects.get(username='bar')
        self.barbar = User.objects.get(username='barbar')
        self.barbarbar = User.objects.get(username='barbarbar')
        self.hoge = AnonymousUser()

        self.group1 = Group.objects.get(pk=1)
        self.group2 = Group.objects.get(pk=2)

        self.article = Article.objects.get(pk=1)

    def test_permissions_created(self):
        # pub_state = draft
        # Author
        self.assert_(self.foo.has_perm('app.view_article', self.article))
        self.assert_(self.foo.has_perm('app.change_article', self.article))
        self.assert_(self.foo.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(not self.bar.has_perm('app.view_article', self.article))
        self.assert_(not self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        self.assert_(not self.barbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(not self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(not self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))

    def test_permission_watched_pub_state_updated(self):
        # pub_state = inspecting
        self.article.pub_state = 'inspecting'
        self.article.save()
        # Author
        self.assert_(self.foo.has_perm('app.view_article', self.article))
        self.assert_(self.foo.has_perm('app.change_article', self.article))
        self.assert_(self.foo.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(self.bar.has_perm('app.view_article', self.article))
        self.assert_(self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        self.assert_(self.barbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(not self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(not self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))

        # pub_state = published
        self.article.pub_state = 'published'
        self.article.save()
        # Author
        self.assert_(self.foo.has_perm('app.view_article', self.article))
        self.assert_(self.foo.has_perm('app.change_article', self.article))
        self.assert_(self.foo.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(self.bar.has_perm('app.view_article', self.article))
        self.assert_(self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        self.assert_(self.barbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))

        # pub_state = draft
        self.article.pub_state = 'draft'
        self.article.save()
        # Author
        self.assert_(self.foo.has_perm('app.view_article', self.article))
        self.assert_(self.foo.has_perm('app.change_article', self.article))
        self.assert_(self.foo.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(not self.bar.has_perm('app.view_article', self.article))
        self.assert_(not self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        self.assert_(not self.barbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(not self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(not self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))

    def test_permission_watched_author_updated(self):
        # pub_state = inspecting
        self.article.pub_state = 'inspecting'
        self.article.author = self.barbarbar
        self.article.save()
        # Author
        self.assert_(self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(self.barbarbar.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(self.bar.has_perm('app.view_article', self.article))
        self.assert_(self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        self.assert_(self.barbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(not self.foo.has_perm('app.view_article', self.article))
        self.assert_(not self.foo.has_perm('app.change_article', self.article))
        self.assert_(not self.foo.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(not self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))

    def test_permission_watched_inspector_updated(self):
        # pub_state = inspecting
        self.article.pub_state = 'inspecting'
        self.article.inspectors.clear()
        self.article.inspectors.add(self.barbarbar)
        self.article.save()
        # Author
        self.assert_(self.foo.has_perm('app.view_article', self.article))
        self.assert_(self.foo.has_perm('app.change_article', self.article))
        self.assert_(self.foo.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(self.foofoofoo.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbarbar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(not self.bar.has_perm('app.view_article', self.article))
        self.assert_(not self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        self.assert_(not self.barbar.has_perm('app.view_article', self.article))
        self.assert_(not self.barbar.has_perm('app.change_article', self.article))
        self.assert_(not self.barbar.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(not self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))

    def test_permission_watched_author_group_updated(self):
        # pub_state = inspecting
        self.article.pub_state = 'inspecting'
        self.article.group = self.group2
        self.article.save()
        # Author
        self.assert_(self.foo.has_perm('app.view_article', self.article))
        self.assert_(self.foo.has_perm('app.change_article', self.article))
        self.assert_(self.foo.has_perm('app.delete_article', self.article))
        # Author group
        self.assert_(self.barbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbar.has_perm('app.change_article', self.article))
        self.assert_(self.barbar.has_perm('app.delete_article', self.article))
        self.assert_(self.barbarbar.has_perm('app.view_article', self.article))
        self.assert_(self.barbarbar.has_perm('app.change_article', self.article))
        self.assert_(self.barbarbar.has_perm('app.delete_article', self.article))
        # Inspector
        self.assert_(self.bar.has_perm('app.view_article', self.article))
        self.assert_(self.bar.has_perm('app.change_article', self.article))
        self.assert_(not self.bar.has_perm('app.delete_article', self.article))
        # Authenticated user
        self.assert_(not self.foofoo.has_perm('app.view_article', self.article))
        self.assert_(not self.foofoo.has_perm('app.change_article', self.article))
        self.assert_(not self.foofoo.has_perm('app.delete_article', self.article))
        self.assert_(not self.foofoofoo.has_perm('app.view_article', self.article))
        self.assert_(not self.foofoofoo.has_perm('app.change_article', self.article))
        self.assert_(not self.foofoofoo.has_perm('app.delete_article', self.article))
        # Anonymous user
        self.assert_(not self.hoge.has_perm('app.view_article', self.article))
        self.assert_(not self.hoge.has_perm('app.change_article', self.article))
        self.assert_(not self.hoge.has_perm('app.delete_article', self.article))
