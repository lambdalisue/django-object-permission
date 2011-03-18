# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
from django import template

register = template.Library()

class IfHasPermNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, perms, obj, user, nodelist_true, nodelist_false, negate, strict=False):
        self.perms, self.obj, self.user = perms, obj, user
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate
        self.strict = strict

    def __repr__(self):
        return "<IfHasPermNode>"

    def render(self, context):
        perms = [perm.resolve(context) for perm in self.perms]
        user = self.user.resolve(context)
        obj = self.obj.resolve(context) if self.obj else None
        result = False
        for perm in perms:
            if user.has_perm(perm, obj):
                result = True
                break
            if not self.strict and user.has_perm(perm):
                result = True
                break
        if (self.negate and not result) or (not self.negate and result):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_ifhasperm(parser, token, negate, strict=False):
    tagname = token.split_contents()[0]
    
    if_elifs = []
    if_spelling = tagname
    endif_spelling = 'end' + tagname
    
    def parse(bits):
        # <perms> of <object> for <user>
        if len(bits) == 5:
            if bits[1] != 'of':
                raise template.TemplateSyntaxError("second argument of %r must be 'of'" % tagname)
            elif bits[3] != 'for':
                raise template.TemplateSyntaxError("forth argument of %r must be 'for'" % tagname)
            object = parser.compile_filter(bits[2])
            user = parser.compile_filter(bits[4])
        # <perms> for <user>
        elif len(bits) == 3:
            if bits[1] != 'for':
                raise template.TemplateSyntaxError("second argument of %r must be 'for'" % tagname)
            object = None
            user = parser.compile_filter(bits[2])
        perms = [parser.compile_filter(perm) for perm in bits[0].split(',')]
        return perms, object, user
    
    class Enders(list):
        def __contains__(self, val):
            return val.startswith('elif') or val in ['else', endif_spelling]
    enders = Enders()
    
    while True:
        bits = token.split_contents()
        command = bits[0]
        bits = bits[1:]
        if command == if_spelling:
            perms, object, user = parse(bits)
            nodelist = parser.parse(enders)
            next_token = parser.next_token()
            if_elifs.append((perms, object, user, nodelist, token))
            if_spelling = 'elif'
            token = next_token
        elif token.contents == 'else':
            nodelist_false = parser.parse((endif_spelling,))
            parser.delete_first_token()
            break
        elif token.contents == endif_spelling:
            nodelist_false = template.NodeList()
            break
    while len(if_elifs) > 1:
        perms, object, user, nodelist_true, token = if_elifs.pop()
        false_node = IfHasPermNode(perms, object, user, nodelist_true, nodelist_false, negate, strict)
        nodelist_false = parser.create_nodelist()
        parser.extend_nodelist(nodelist_false, false_node, token)
    perms, object, user, nodelist_true, token = if_elifs[0]
    return IfHasPermNode(perms, object, user, nodelist_true, nodelist_false, negate, strict)

@register.tag('ifhsp')
def ifhasperm(parser, token):
    """
    Outputs the contents of the block if the user has permission of object.

    Examples::

        {% ifhsp 'change_object' of object for user %}
            ...
        {% elif 'delete_object' of object for user %}
            ...
        {% elif 'add_object' for user %}
            ...
        {% else %}
            ...
        {% endifhsp %}

        {% ifnothsp 'change_object' of object for user %}
            ...
        {% elif 'delete_object' of object for user %}
            ...
        {% elif 'add_object' for user %}
            ...
        {% else %}
            ...
        {% endifnothsp %}
    """
    return do_ifhasperm(parser, token, False)

@register.tag('ifnothsp')
def ifnothasperm(parser, token):
    """
    Outputs the contents of the block if the user has permission of object.
    See ifhasperm.
    """
    return do_ifhasperm(parser, token, True)

@register.tag('ifhsps')
def ifhasperm_strict(parser, token):
    """
    Outputs the contents of the block if the user has permission of object.

    Examples::

        {% ifhsps 'change_object' of object for user %}
            ...
        {% elif 'delete_object' of object for user %}
            ...
        {% elif 'add_object' for user %}
            ...
        {% else %}
            ...
        {% endifhsps %}

        {% ifnothsps 'change_object' of object for user %}
            ...
        {% elif 'delete_object' of object for user %}
            ...
        {% elif 'add_object' for user %}
            ...
        {% else %}
            ...
        {% endifnothsps %}
    """
    return do_ifhasperm(parser, token, False, strict=True)

@register.tag('ifnothsps')
def ifnothasperm_strict(parser, token):
    """
    Outputs the contents of the block if the user has permission of object.
    See ifhasperm.
    """
    return do_ifhasperm(parser, token, True, strict=True)