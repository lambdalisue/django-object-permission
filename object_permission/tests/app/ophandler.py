#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Object permission handler for model of testing app


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
from observer import watch
from object_permission import site
from object_permission.handlers import ObjectPermHandlerBase

from models import Article

class ArticleObjectPermHandler(ObjectPermHandlerBase):
    def created(self):
        # Watch related fields with observer
        self._pub_state_watcher = watch(self.obj, 'pub_state', self._pub_state_updated)
        self._author_watcher = watch(self.obj, 'author', self._author_updated)
        self._inspectors_watcher = watch(self.obj, 'inspectors', self._inspectors_updated)
        # Call updated
        self.updated()

    def updated(self):
        # Reset all permissions for this object
        self.mediator.reset()
        # Author has manager permission
        self.mediator.manager(self.obj.author)
        if self.obj.pub_state == 'draft':
            # No-one can view the object
            self.mediator.reject(self.obj.inspectors)
            self.mediator.reject(None)
            self.mediator.reject('anonymous')
        else:
            # Inspector has editor permission
            self.mediator.editor(self.obj.inspectors)
            # Authenticated user has viewer permission
            self.mediator.viewer(None)
            if self.obj.pub_state == 'inspecting':
                # Anonymous user has no permissions
                self.mediator.reject('anonymous')
            else:
                # Article published
                self.mediator.viewer('anonymous')

    def deleted(self):
        # Remove watchers
        self._pub_state_watcher.unwatch()
        self._author_watcher.unwatch()
        self._inspectors_watcher.unwatch()

    def _pub_state_updated(self, sender, obj, attr):
        self.updated()

    def _author_updated(self, sender, obj, attr):
        # Reset object permissioin because to lazy to find previous author
        # and remove the permission lol.
        self.mediator.reset()
        self.updated()

    def _inspectors_updated(self, sender, obj, attr):
        # Reset object permissioin because to lazy to find previous inspectors
        # and remove the permission lol.
        self.mediator.reset()
        self.updated()

# Register
site.register(Article, ArticleObjectPermHandler)
