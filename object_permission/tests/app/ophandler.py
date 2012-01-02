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
from object_permission import site
from object_permission.handlers import ObjectPermHandler

from models import Article

class ArticleObjectPermHandler(ObjectPermHandler):
    def setup(self):
        # Watch related fields with observer
        self.watch('pub_state')
        self.watch('author')
        self.watch('inspectors')

    def updated(self, attr):
        # Author has manager permission
        self.manager(self.instance.author)
        if self.instance.pub_state == 'draft':
            # No-one can view the object
            self.reject(self.instance.inspectors)
            self.reject(None)
            self.reject('anonymous')
        else:
            # Inspector has editor permission
            self.editor(self.instance.inspectors)
            # Authenticated user has viewer permission
            self.viewer(None)
            if self.instance.pub_state == 'inspecting':
                # Anonymous user has no permissions
                self.reject('anonymous')
            else:
                # Article published
                self.viewer('anonymous')
# Register
site.register(Article, ArticleObjectPermHandler)
