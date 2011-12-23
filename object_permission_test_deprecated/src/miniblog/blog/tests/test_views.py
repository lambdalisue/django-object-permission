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
from django.test import TestCase
from ..models import Entry

class EntryViewTestCase(TestCase):
    fixtures = ['test_user.yaml', 'test_entry.yaml']

    def test_list_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_detail_get(self):
        # Anonymous user doesn't have view permission
        response = self.client.get('/foo/')
        self.assertRedirects(response, '/accounts/login/?next=/foo/')

        # Authenticated user has view permission
        assert self.client.login(username='foo', password='password')
        response = self.client.get('/foo/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_detail_get_invalid(self):
        # Permission doesn't affect object which doesn't exist
        response = self.client.get('/unknown/')
        self.assertEqual(response.status_code, 404)

    def test_create_get(self):
        response = self.client.get('/create/')
        # Anonymous user doesn't have create permission
        self.assertRedirects(response, '/accounts/login/?next=/create/')
    
        # Authenticated user has add permission
        assert self.client.login(username='foo', password='password')
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_create_post(self):
        # Anonymous user doesn't have add permission
        response = self.client.post('/create/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertRedirects(response, '/accounts/login/?next=/create/')
        
        # Authenticated user has add permission
        assert self.client.login(username='foo', password='password')
        response = self.client.post('/create/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertEqual(response.status_code, 302)
        assert Entry.objects.filter(title='foobar').exists()
        self.client.logout()

    def test_create_post_invalid(self):
        assert self.client.login(username='foo', password='password')
        response = self.client.post('/create/', {
                'title': '', 'body': ''
            })
        self.assertEqual(response.status_code, 200)
        assert 'This field is required' in response.content
        self.client.logout()

    def test_update_get(self):
        # Anonymous user doesn't have change permission
        response = self.client.get('/update/2/')
        self.assertRedirects(response, '/accounts/login/?next=/update/2/')

        # Non author user doesn't have change permission
        assert self.client.login(username='bar', password='password')
        response = self.client.get('/update/2/')
        self.assertEqual(response.status_code, 403)

        # Author has change permission
        assert self.client.login(username='foo', password='password')
        response = self.client.get('/update/2/')
        self.assertEqual(response.status_code, 200)

        # superuser has all permissions
        assert self.client.login(username='admin', password='password')
        response = self.client.get('/update/2/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_update_get_invalid(self):
        # Permission doesn't affect object which doesn't exist
        response = self.client.get('/update/999/')
        self.assertEqual(response.status_code, 404)

    def test_update_post(self):
        # Anonymous user doesn't have change permission
        response = self.client.post('/update/2/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertRedirects(response, '/accounts/login/?next=/update/2/')

        # Non author user doesn't have change permission
        assert self.client.login(username='bar', password='password')
        response = self.client.post('/update/2/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertEqual(response.status_code, 403)

        # Author user has change permission
        assert self.client.login(username='foo', password='password')
        response = self.client.post('/update/2/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.get(pk=2).title, 'foobar')
        self.assertEqual(Entry.objects.get(pk=2).body, 'foobar')

        # superuser has all permissions
        assert self.client.login(username='admin', password='password')
        response = self.client.post('/update/2/', {
                'title': 'foobar2', 'body': 'foobar2'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.get(pk=2).title, 'foobar2')
        self.assertEqual(Entry.objects.get(pk=2).body, 'foobar2')
        self.client.logout()

    def test_update_post_invalid(self):
        assert self.client.login(username='foo', password='password')
        response = self.client.post('/update/2/', {
                'title': '', 'body': ''
            })
        self.assertEqual(response.status_code, 200)
        assert 'This field is required' in response.content
        self.client.logout()

    def test_delete_get(self):
        # Anonymous user doesn't have delete permission
        response = self.client.get('/delete/2/')
        self.assertRedirects(response, '/accounts/login/?next=/delete/2/')

        # Non author user doesn't have delete permission
        assert self.client.login(username='bar', password='password')
        response = self.client.get('/delete/2/')
        self.assertEqual(response.status_code, 403)

        # Author user have delete permission
        assert self.client.login(username='foo', password='password')
        response = self.client.get('/delete/2/')
        self.assertEqual(response.status_code, 200)

        # superuser have all permissions
        assert self.client.login(username='admin', password='password')
        response = self.client.get('/delete/2/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_delete_get_invalid(self):
        response = self.client.get('/delete/999/')
        self.assertEqual(response.status_code, 404)

    def test_delete_post(self):
        # Anonymous user doesn't have delete permission
        response = self.client.post('/delete/2/')
        self.assertRedirects(response, '/accounts/login/?next=/delete/2/')

        # Non author user doesn't have delete permission
        assert self.client.login(username='bar', password='password')
        response = self.client.post('/delete/2/')
        self.assertEqual(response.status_code, 403)

        # Author user has delete permission
        assert self.client.login(username='foo', password='password')
        response = self.client.post('/delete/2/')
        self.assertEqual(response.status_code, 302)
        assert not Entry.objects.filter(pk=2).exists()

        # superuser has all permissions
        assert self.client.login(username='admin', password='password')
        response = self.client.post('/delete/3/')
        self.assertEqual(response.status_code, 302)
        assert not Entry.objects.filter(pk=3).exists()
        self.client.logout()
