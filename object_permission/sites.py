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
from django.conf import settings
from django.db.models import Model

class AlreadyRegistered(Exception):
    pass
class NotRegistered(Exception):
    pass

class ObjectPermSite(object):
    """Manager class of ObjectPermHandler"""
    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, handler_class=None):
        """registers the given model(s) with the given handler class.
        
        The model(s) should be Model classes, not instances.

        If a model is already registered, this will raise AlreadyRegistered
        """
        if handler_class is None:
            handler_class = settings.OBJECT_PERMISSION_DEFAULT_HANDLER_CLASS
        if issubclass(model_or_iterable, Model):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered('The mode %s is already registered' % model.__name__)
            
            handler_class.bind(model)
            self._registry[model] = handler_class

    def unregister(self, model_or_iterable):
        """unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered
        """
        if issubclass(model_or_iterable, Model):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            self._registry[model].unbind(model)
            del self._registry[model]

site = ObjectPermSite()
