#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Base module of object-permission handler


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

from ..mediators import ObjectPermMediator
class ObjectPermHandlerBase(object):
    """Base ObjectPermHandler"""
    def __init__(self, model):
        self.model = model

    def bind(self):
        """bind signals and recivers"""
        post_save.connect(self._post_save_reciever, sender=self.model, weak=False)
        post_delete.connect(self._post_delete_reciver, sender=self.model, weak=False)

    def unbind(self):
        """unbind signals and recivers."""
        post_save.disconnect(self._post_save_reciever, sender=self.model)
        post_delete.disconnect(self._post_delete_reciver, sender=self.model)

    def _post_save_reciever(self, sender, instance, created, **kwargs):
        self.obj = instance
        self.mediator = ObjectPermMediator(self.obj)
        if created:
            self.created()
        else:
            self.updated()
    def _post_delete_reciver(self, sender, instance, **kwargs):
        self.obj = instance
        self.mediator = ObjectPermMediator(self.obj)
        self.deleted()


    def created(self):
        """called when object is created"""
        pass

    def updated(self):
        """called when object is updated"""
        pass
    
    def deleted(self):
        """called when object is deleted"""
        pass

