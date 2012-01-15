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

See `object_permission_test <https://github.com/lambdalisue/django-object-permission/tree/master/object_permission_test/>`_
for more detail. If you want to see Old-style storategy, see `README_old.rst <https://github.com/lambdalisue/django-object-permission/tree/master/README_old.rst>`_ or
`object_permission_test_deprecated <https://github.com/lambdalisue/django-object-permission/tree/master/object_permission_test_deprecated/>`_

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
    from object_permission.handlers import ObjectPermHandler

    from models import Entry

    class EntryObjectPermHandler(ObjectPermHandler):
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

        # decorate 'dispatch' method without method_decorator
        @permission_required('blog.view_entry')
        def dispatch(self, *args, **kwargs):
            return super(EntryDetailView, self).dispatch(*args, **kwargs)

    # You can use the decorator as View class decorator
    # Then automatically decorate 'dispatch' method of the View
    @permission_required('blog.add_entry')
    class EntryCreateView(CreateView):
        form_class = EntryForm
        model = Entry

    @permission_required('blog.change_entry')
    class EntryUpdateView(UpdateView):
        form_class = EntryForm
        model = Entry

    @permission_required('blog.delete_entry')
    class EntryDeleteView(DeleteView):
        model = Entry
        def get_success_url(self):
            return reverse('blog-entry-list')

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

    will removed in version 0.5

``OBJECT_PERMISSION_MODIFY_FUNCTION`` (deprecated)
    set the name of function when object is saved for modify object permission for the object.
    the default value is ``modify_object_permission``

``OBJECT_PERMISSION_MODIFY_M2M_FUNCTION`` (deprecated)
    set the name of function when object's ManyToMany relation is updated for modify object permission
    for the object. the default value is ``modify_object_permission_m2m``
