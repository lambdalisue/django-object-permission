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
from base import ObjectPermHandler

class AuthorObjectPermHandler(ObjectPermHandler):
    """ObjectPermHandler for model which has author field

    This handler contribute..

        1.  Manager permission to instance author
        2.  Viewer permission to authenticated user
        3.  Viewer permission to anonymous user if reject_anonymous is False

    """
    author_field = 'author'
    reject_anonymous = False

    def get_author(self):
        """get author field value"""
        return getattr(self.instance, self.author_field)

    def setup(self):
        # watch author field
        self.watch(self.author_field)

    def updated(self, attr):
        # Author has full access
        self.manager(self.get_author())
        # Authenticated user can view
        self.viewer(None)
        if self.reject_anonymous:
            self.reject('anonymous')
        else:
            self.viewer('anonymous')
