#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Default Object permission handler for model


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
from django.contrib.auth.models import User
from base import ObjectPermHandler

class AuthenticatedObjectPermHandler(ObjectPermHandler):
    """ObjectPermHandler for model

    This handler contribute..

        1.  Manager permission to authenticated staff user
        2.  Editor permission to authenticated user
        3.  Viewer permission to anonymous user

    """
    def updated(self, attr):
        # staff user has full access
        staff_users = User.objects.filter(staff=True)
        self.manager(staff_users.iterator())
        # Authenticated user can edit
        self.editor(None)
        # Anonymous user can view
        self.viewer('anonymous')

def _recall_updated_reciver(sender, instance, **kwargs):
    # Recall updated method of all AuthenticatedObjectPermHandler instance
    AuthenticatedObjectPermHandler.update()
post_save.connect(_recall_updated_reciver, User)
post_delete.connect(_recall_updated_reciver, User)
