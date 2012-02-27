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
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Article(models.Model):
    PUB_STATES = (
            ('draft',   'draft'),
            ('inspecting', 'inspecting'),
            ('published', 'published'),
        )
    pub_state = models.CharField(
            'publish status', max_length=10, 
            choices=PUB_STATES, default='draft')

    title = models.CharField('title', max_length=200, default='No title')
    body = models.TextField('body', blank=True, default='')

    inspectors = models.ManyToManyField(User, related_name='inspected_articles')
    
    group = models.ForeignKey(Group, related_name='articles', blank=True, null=True)

    author = models.ForeignKey(User, related_name='articles')

    def __unicode__(self):
        return self.title
