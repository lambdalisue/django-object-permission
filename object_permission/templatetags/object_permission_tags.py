#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
templatetag for django-object-permission

Django 1.2 template tag that supports {% elif %} branches and
'of' operator for checking object permission.


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
import warnings

from django import template
from django.template import Node, VariableDoesNotExist
from django.template.smartif import infix
from django.template.smartif import IfParser
from django.template.smartif import OPERATORS as _OPERATORS
from django.template.defaulttags import TemplateLiteral

register = template.Library()

OPERATORS = dict(_OPERATORS,
    of=infix(10, lambda context, x, y: 
        template.resolve_variable('request', context).user.has_perm(x.eval(context), y.eval(context)))
)

class ObjectPermissionIfParser(IfParser):
    def translate_token(self, token):
        try:
            op = OPERATORS[token]
        except (KeyError, TypeError):
            return self.create_var(token)
        else:
            return op()
class TemplateObjectPermissionIfParser(ObjectPermissionIfParser):
    error_class = template.TemplateSyntaxError

    def __init__(self, parser, *args, **kwargs):
        self.template_parser = parser
        return super(TemplateObjectPermissionIfParser, self).__init__(*args, **kwargs)

    def create_var(self, value):
        return TemplateLiteral(self.template_parser.compile_filter(value), value)
    
class IfBranch(object):
    def __init__(self, var, node_list):
        self.var = var
        self.node_list = node_list

class IfNode(Node):
    def __init__(self, branches):
        self.branches = branches

    def __repr__(self):
        return "<If node>"

    def __iter__(self):
        for n in self.branches:
            for node in n:
                yield node

    def render(self, context):
        for n in self.branches:
            var = n.var
            if var != True:
                try:
                    var = var.eval(context)
                except VariableDoesNotExist:
                    var = None
            if var:
                return n.node_list.render(context)
                break
        return ""

@register.tag('ifhsp')
def do_ifhsp(parser, token):
    warnings.warn('deprecated. use `pif` insted', DeprecationWarning)
    return do_if(parser, token)
@register.tag('pif')
def do_if(parser, token):
    """
    Django 1.2 template tag that supports {% elif %} branches and
    'of' operator for checking object permission.

    .. Warning::
        This template tag assumed that context has 'request' so make sure your
        ``TEMPLATE_CONTEXTS`` is like below::
        
            TEMPLATE_CONTEXT_PROCESSORS = (
                "django.core.context_processors.auth",           # This one is required
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",        # This one is required
            )

    Usage::

        {% pif 'blogs.add_entry' of None or user.is_staff %}
            You can add post
        {% elif 'blogs.change_entry' of object or 'blogs.delete_entry' of object %}
            You can update/delete this entry
        {% endpif %}
    """
    class Enders(list):
        def __init__(self, endtag):
            self.endtag = endtag
        def __contains__(self, val):
            return val.startswith('elif') or val in ('else', self.endtag)
    
    name = contents = token.split_contents()[0]
    endtag = "end%s" % name
    enders = Enders(endtag)
    branches = []
    
    while True:
        contents = token.split_contents()
        bits = contents[1:]
        if contents[0] in (name, "elif"):
            var = TemplateObjectPermissionIfParser(parser, bits).parse()
            nodelist = parser.parse(enders)
            next_token = parser.next_token()
            branches.append(IfBranch(var, nodelist))
            token = next_token
        elif token.contents == 'else':
            nodelist = parser.parse((endtag,))
            parser.delete_first_token()
            branches.append(IfBranch(True, nodelist))
            break
        elif token.contents == endtag:
            break

    return IfNode(branches)
