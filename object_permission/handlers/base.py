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

from observer import watch

from ..mediators import ObjectPermMediator

class ObjectPermHandlerBase(ObjectPermMediator):
    """Base class of ObjectPermHandler
    
    ObjectPermHandler is a subclass of ObjectPermMediator so the class has all
    attributes/methods of the ObjectPermMediator

    Bind the model class and ObjectPermHandler then automatically 'setup' and 
    'teardown' method of the class is called when the instance of the model is
    created/deleted.

    watch attrs in 'setup' method then automatically 'updated' method is called
    when the watched attr is updated.
    """
    def __init__(self, instance):
        super(ObjectPermHandlerBase, self).__init__(instance)
        self.model = instance.__class__

    @classmethod
    def bind(cls, model):
        """bind model and this handler"""
        post_save.connect(cls._post_save_reciever, sender=model, weak=False)
        post_delete.connect(cls._post_delete_reciver, sender=model, weak=False)

    @classmethod
    def unbind(cls, model):
        """unbind model and this handler"""
        post_save.disconnect(cls._post_save_reciever, sender=model)
        post_delete.disconnect(cls._post_delete_reciver, sender=model)

    @classmethod
    def _post_save_reciever(cls, sender, instance, created, **kwargs):
        # register the instance to this class
        if created or cls.get(instance) is None:
            cls._register(instance)

    @classmethod
    def _post_delete_reciver(cls, sender, instance, **kwargs):
        # unregister the instance from this class
        cls._unregister(instance)

    @classmethod
    def _register(cls, instance):
        # create new handler instance
        self = cls(instance)
        # register the handler instance to cls
        if not hasattr(cls, '_handlers'):
            cls._handlers = {}
        cls._handlers[instance] = self
        # call pre setup method
        self._setup()
        # call pre updated method
        self._updated(attr=None)

    @classmethod
    def _unregister(cls, instance):
        # if no handler is registered, just ignore
        if not hasattr(cls, '_handlers'):
            return
        self = cls._handlers[instance]
        # call pre teardown method
        self._teardown()
        del cls._handlers[instance]

    @classmethod
    def get(cls, instance):
        if not hasattr(cls, '_handlers'):
            cls._handlers = {}
        return cls._handlers.get(instance)

    @classmethod
    def update(cls):
        """call 'updated' method of all instance of this class"""
        if not hasattr(cls, '_handlers'):
            return
        for model, handler in cls._handlers.iteritems():
            handler._updated(attr=None)

    def _setup(self):
        raise NotImplementedError
    def _teardown(self):
        raise NotImplementedError
    def _updated(self):
        raise NotImplementedError

class ObjectPermHandler(ObjectPermHandlerBase):
    def __init__(self, instance):
        super(ObjectPermHandler, self).__init__(instance)
        self._watchers = {}

    def _watch_update_reciver(self, sender, obj, attr):
        # update instance (because self.instance is not fresh)
        self.instance = obj
        # call pre updated method
        self._updated(attr)

    def _watch(self, instance, attr, callback):
        """Watch instance attr and call callback and register the watcher"""
        if instance not in self._watchers:
            self._watchers[instance] = []
        watcher = watch(instance, attr, callback)
        self._watchers[instance].append(watcher)

    def _unwatch(self, instance=None):
        """Unwatch watchers of instance."""
        if instance:
            if instance in self._watchers:
                del self._watchers[instance]
        else:
            # unwatch all watchers registered in this class instance
            self._watchers = {}

    def watch(self, attr, instance=None):
        """Watch instance attr and call 'updated' method of this class"""
        if instance is None:
            instance = self.instance
        self._watch(instance ,attr, self._watch_update_reciver)

    def _setup(self):
        """pre setup method"""
        self.setup()

    def _teardown(self):
        """pre teardown method"""
        # unwatch all watchers registered in this class instance
        self._unwatch(instance=None)
        self.teardown()

    def _updated(self, attr):
        """pre updated method"""
        # reset object permission of the instance
        self.reset()
        # call updated method
        self.updated(attr)

    def setup(self):
        """called when the bind model instance is created."""
        pass

    def updated(self, attr):
        """called when watched attr of the instance is updated"""
        raise NotImplementedError

    def teardown(self):
        """called when the bind model instance is deleted."""
        pass
