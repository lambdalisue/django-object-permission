#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Object permission handler for model which has author field


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
try:
    from observer import watch
except ImportError:
    raise ImportError("AuthorObjectPermHandler required 'django-observer' installed")

from base import ObjectPermHandlerBase

class AuthorObjectPermHandler(ObjectPermHandlerBase):
    """ObjectPermHandler for model which has author field

    This handler contribute..

        1.  Manager permission to instance author
        2.  Viewer permission to authenticated user
        3.  Viewer permission to anonymous user if reject_anonymous is False

    """
    author_field = 'author'
    reject_anonymous = False

    def __del__(self):
        self.deleted()

    def unbind(self):
        super(AuthorObjectPermHandler, self).unbind()
        # Remove watcher
        self._author_field_watcher.unwatch()

    def get_author(self):
        return getattr(self.obj, self.author_field)

    def created(self):
        # Watch author change
        self._author_field_watcher = \
                watch(self.obj, self.author_field, self._author_field_changed)
        # Call updated method
        self.updated()

    def updated(self):
        # Author has full access
        self.mediator.manager(self.get_author())
        # Authenticated user can view
        self.mediator.viewer(None)
        if self.reject_anonymous:
            self.mediator.reject('anonymous')
        else:
            self.mediator.viewer('anonymous')

    def deleted(self):
        # Remove watcher
        self._author_field_watcher.unwatch()

    def _author_field_changed(self, sender, instance, attr):
        # reset all object permissions for obj
        self.mediator.reset()
        self.updated()
