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
from django.db.models.signals import pre_save
from django.db.models.signals import post_save

class FieldObserver(object):

class Observer(object):
    @classmethod
    def watch(cls, obj, callback):
        if hasattr(obj, 'model'):
            # Django field
            name = obj.name
            model = obj.model
            cls._watch_field(name, model, callback)
    @classmethod
    def _watch_field(cls, name, model, callback):
        self = Observer()
        self.field = model._meta.get_field_by_name(name)[0]
        self.model = self.field.model
        self.callback = callback
        pre_save.connect(self._pre_save_reciver, sender=self.model)
        pre_save.connect(self._post_save_reciver, sender=self.model)

    def _pre_save_reciver(self, sender, instance, **kwargs):
        if sender != self.model:
            return
        self._previous = getattr(instance, self.field.name)
    def _post_save_reciver(self, sender, instance, created, **kwargs):
        if sender != self.model:
            return
        if created or getattr(instance, self.field.name) != self._previous:
            self.callback(instance)
