``django-object-permissiono`` apply object permission feature to Django models

Install
===========================================
::

	sudo pip install django-object-permission

or::

    sudo pip install git+git://github.com/lambdalisue/django-object-permission.git#egg=django-object-permission


How to Use
==========================================

1.  Append 'object_permission' to ``INSTALLED_APPS``

2.  Append 'object_permission.backends.ObjectPermBackend' to ``AUTHENTICATION_BACKENDS``

3.  Add 'ophandler.py' to your app directory like 'admin.py'

4.  Write model specific ObjectPermHandler and register it with model to ``object_permission.site``

See `object_permission_test <https://github.com/lambdalisue/django-object-permission/object_permission_test/>`_
for more detail. If you want to see Old-style storategy, see `README_old.rst <https://github.com/lambdalisue/django-object-permission/README_old.rst>`_ or
`object_permission_test_deprecated <https://github.com/lambdalisue/django-object-permission/object_permission_test_deprecated/>`_

Example mini blog app
=========================================

``models.py``::
	
	from django.db import models
	from django.contrib.auth.models import User

	# django-author: useful for adding automatically update author field
	from author.decorators import with_author
	
	@with_author
	class Entry(models.Model):
		PUB_STATES = (
			('public', 'public entry'),
			('protected', 'login required'),
			('private', 'secret entry'),
		)
		pub_state = models.CharField('publish status', choices=PUB_STATES)
		title = models.CharField('title', max_length=140)
		body = models.TextField('body')

		# ...

``ophandler.py``::

    from object_permission import site
    # AuthorObjectPermHandler need 'django-observer' and required 'author'
    # field (the author field is automatically added by 'with_author' decorator)
    from object_permission.handlers.author import AuthorObjectPermHandler

    from models import Entry

    class EntryObjectPermHandler(AuthorObjectPermHandler):
        """Add permission of obj...

        Author:
            Full control (view, change, delete)
        Authenticated user:
            Can view (view)
        Anonymous user:
            Cannot view
        """
        reject_anonymous = True
    # Register to object_permission site like django.contrib.admin
    site.register(Entry, EntryObjectPermHandler)
    
``views.py``::

    from django.views.generic import ListView
    from django.views.generic import DetailView
    from django.views.generic import CreateView
    from django.views.generic import UpdateView
    from django.views.generic import DeleteView
    from django.core.urlresolvers import reverse

    from object_permission.decorators import permission_required

    from models import Entry
    from forms import EntryForm

    class EntryListView(ListView):
        model = Entry

    class EntryDetailView(DetailView):
        model = Entry
        slug_field = 'title'

        @permission_required('blog.view_entry')
        def dispatch(self, *args, **kwargs):
            return super(EntryDetailView, self).dispatch(*args, **kwargs)

    class EntryCreateView(CreateView):
        form_class = EntryForm
        model = Entry

        @permission_required('blog.add_entry')
        def dispatch(self, *args, **kwargs):
            return super(EntryCreateView, self).dispatch(*args, **kwargs)

    class EntryUpdateView(UpdateView):
        form_class = EntryForm
        model = Entry

        @permission_required('blog.change_entry')
        def dispatch(self, *args, **kwargs):
            return super(EntryUpdateView, self).dispatch(*args, **kwargs)

    class EntryDeleteView(DeleteView):
        model = Entry
        def get_success_url(self):
            return reverse('blog-entry-list')

        @permission_required('blog.delete_entry')
        def dispatch(self, *args, **kwargs):
            return super(EntryDeleteView, self).dispatch(*args, **kwargs)

``index.html``::

	{% load object_permission_tags %}
	<html>
	<head>
		<title>django-object-permission example</title>
	</head>
	<body>
		{% pif 'blog.add_entry' of None or 'blog.change_entry' of object or 'blog.delete_entry' of object %}
		<!-- displayed only user who has `blog.add_entry` permission, 
			`blog.change_entry` permision for object or
			`blog.delete_entry` permission for object -->
			<h2>Toolbox</h2>
			{% pif 'blog.add_entry' of object %}
				<!-- displayed only user who has `blog.add_entry` permission -->
				<a href="{% url 'blog-entry-create' %}">Add New Entry</a>
			{% endpif %}
			{% pif object and 'blog.change_entry' of object %}
				<!-- displayed only user who has `blog.change_entry` permission for object -->
				<a href="{% url 'blog-entry-update' object.pk %}">Change this entry</a>
			{% endpif %}
			{% pif object and 'blog.delete_entry' of object %}
				<!-- displayed only user who has `blog.delete_entry` permission for object -->
				<a href="{% url 'blog-entry-delete' object.pk %}">Delete this entry</a>
			{% endpif%}
		{% endpif %}
	</body>
	</html>

Settings
=========================================
``OBJECT_PERMISSION_EXTRA_DEFAULT_PERMISSIONS``
    A list of extra default permission for all models. Django contribute
    'add', 'change' and 'delete' permission for all models as default.

    Default: ``['view']``

``OBJECT_PERMISSION_BUILTIN_TEMPLATETAGS``
    If this is True, then ``pif`` will be builtin templatetags which mean you don't
    need to add ``{% load object_permission_tags %}`` before use ``pif`` tag.

    Default: ``True``

``OBJECT_PERMISSION_AUTODISCOVER``
    To enable autodiscover feature. object permission automatically search 'ophandler'
    (or ``OBJECT_PERMISSION_HANDLER_MODULE_NAME``) module for each apps and load.

    Default: ``True``

``OBJECT_PERMISSION_HANDLER_MODULE_NAME``
    Used for searching object permission handler module for each apps.

    Default: ``'ophandler'``

``OBJECT_PERMISSION_DEPRECATED``
    If this is True then all deprecated feature is loaded. You should not turnd on
    this unless your project is too large to do refactaring because deprecated feature 
    is no longer supported and limited.

``OBJECT_PERMISSION_MODIFY_FUNCTION`` (deprecated)
    set the name of function when object is saved for modify object permission for the object.
    the default value is ``modify_object_permission``

``OBJECT_PERMISSION_MODIFY_M2M_FUNCTION`` (deprecated)
    set the name of function when object's ManyToMany relation is updated for modify object permission
    for the object. the default value is ``modify_object_permission_m2m``
