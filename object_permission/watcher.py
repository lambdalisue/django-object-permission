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
from django.db.models.signals import post_save
from django.db.models.signals import post_delete

from observer import watch

from mediators import ObjectPermMediator

class WatcherBase(ObjectPermMediator):
    reset_required_attrs = []

    def __init__(self, obj):
        self.obj = obj
        self.model = obj.__class__
        self._watchers = []
        # Add recivers
        post_save.connect(self._post_save_reciver, 
                          sender=self.model, weak=False)
        post_delete.connect(self._post_delete_reciver,
                            sender=self.model, weak=False)

    def watch(self, attr, callback=None):
        if not callback:
            callback = self._attr_updated_reciver
        watcher = watch(self.obj, attr, callback)
        self._watchers.append(watcher)

    def unwatch_all(self):
        for watcher in self._watchers:
            watcher.unwatch()
        self._watchers = []
        
    def _post_save_reciver(self, sender, instance, created, **kwargs):
        if created:
            self.prepare(instance)
            self.updated(instance, None)
    def _post_delete_reciver(self, sender, instance, **kwargs):
        self.unwatch_all()
    def _attr_updated_reciver(self, sender, instance, attr):
        self._pre_updated(instance, attr)

    def prepare(self, instance):
        pass
    def updated(self, instance, attr):
        pass

    def _pre_updated(self, instance, attr):
        # is this attr required reset all object permission of this object?
        if attr in self.reset_required_attrs:
            self.reset()
        self.updated(instance, attr)
