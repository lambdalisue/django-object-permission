# vim: set fileencoding=utf8:
"""
Mini blog models

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
__VERSION__ = "0.1.0"
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import ugettext_lazy as _

class Entry(models.Model):
    """mini blog entry model
    
    >>> entry = Entry()

    # Attribute test
    >>> assert hasattr(entry, 'title')
    >>> assert hasattr(entry, 'body')
    >>> assert hasattr(entry, 'created_at')
    >>> assert hasattr(entry, 'updated_at')

    # Function test
    >>> assert callable(getattr(entry, '__unicode__'))
    >>> assert callable(getattr(entry, 'get_absolute_url'))
    """
    title = models.SlugField(_('title'), unique=True)
    body = models.TextField(_('body'))

    created_at = models.DateTimeField(_('date and time created'),
            auto_now_add=True)
    updated_at = models.DateTimeField(_('date and time updated'),
            auto_now=True)

    author = models.ForeignKey(User, verbose_name=_('author'), editable=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blogs-entry-detail', (), {'slug': self.title})

    def clean(self):
        """custom validation"""
        from django.core.exceptions import ValidationError
        if self.title in ('create', 'update', 'delete'):
            raise ValidationError(
                    """The title cannot be 'create', 'update' or 'delete'""")

from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
def _is_in_test_at_loggerheads():
    # Automatical adding permission raise FAIL on django.contrib.auth.tests.backends.BackendTest
    # So ignore if 'object_permission.backends.ObjectPermBackend' is not
    # in AUTHENTICATION_BACKENDS (because the test overwrite the setting)
    if 'object_permission.backends.ObjectPermBackend' not in settings.AUTHENTICATION_BACKENDS:
        return True
    # Automatical adding permission raise FAIL on django.contrib.auth.tests.backends.SimpleRowlevelBackendTest
    # So ignore if 'django.contrib.auth.tests.auth_backends.SimpleRowlevelBackend' is 
    # in AUTHENTICATION_BACKENDS (because the test overwrite the setting)
    elif 'django.contrib.auth.tests.auth_backends.SimpleRowlevelBackend' in settings.AUTHENTICATION_BACKENDS:
        return True
    return False
def _add_permission_to_user(sender, instance, created, **kwargs):
    if _is_in_test_at_loggerheads():
        # adding permission may raise FAIL so ignore
        return
    if not created:
        return
    ct = ContentType.objects.get_for_model(Entry)
    # Note:
    #   the permission may not exists on syncdb so 'get_or_create' is used insted of 'get'
    add_entry = Permission.objects.get_or_create(content_type=ct, codename='add_entry')[0]
    instance.user_permissions.add(add_entry)
post_save.connect(_add_permission_to_user, sender=User)
