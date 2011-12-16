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
from django.utils.text import ugettext_lazy as _

from author.decorators import with_author

@with_author
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

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog-entry-detail', (), {'slug': self.title})

    def clean(self):
        """custom validation"""
        from django.core.exceptions import ValidationError
        if self.title in ('create', 'update', 'delete'):
            raise ValidationError(
                    """The title cannot be 'create', 'update' or 'delete'""")

    def modify_object_permission(self, mediator, created):
        """this function is automatically called by object-permission"""
        mediator.manager(self, self.author)
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
