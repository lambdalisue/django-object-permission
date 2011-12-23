#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Extra settings for object-permissions


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

def set_default(name, value):
    setattr(settings, name, getattr(settings, name, value))

set_default(
    'OBJECT_PERMISSION_DEFAULT_HANDLER_CLASS', 
    'object_permission.handlers.authenticated.AuthenticatedObjectPermHandler')
set_default('OBJECT_PERMISSION_EXTRA_DEFAULT_PERMISSIONS', ['view'])
set_default('OBJECT_PERMISSION_BUILTIN_TAGS', True)
set_default('OBJECT_PERMISSION_AUTODISCOVER', True)
