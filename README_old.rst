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
3.  run ``manage.py syncdb``
4.  Add ``modify_object_permission(mediator, created)`` and ``modify_object_permission_m2m(mediator, sender, model, pk_set, removed)`` to the target model at ``models.py``
5.  Use ``object_permission.decorators.permission_required(parm, queryset)`` to filtering view or whatever


Example mini blog app
=========================================

``models.py``::
	
	from django.db import models
	from django.contrib.auth.models import User
	from object_permission.mediators import ObjectPermissionMediator as Mediator
	
	class Entry(models.Model):
		PUB_STATES = (
			('public', 'public entry'),
			('protected', 'login required'),
			('private', 'secret entry'),
		)
		pub_state = models.CharField('publish status', choices=PUB_STATES)
		title = models.CharField('title', max_length=140)
		body = models.TextField('body')
		author = models.ForeignKey(User, verbose_name='author')

		# ...

		# The method below is called every after when object is saved
		def modify_object_permission(self, mediator, created):
			# be author to manager (has `view`, `add`, `change`, `delete` permission)
			mediator.manager(self, self.author)
			
			if self.pub_state == 'public':
				# be viewer (has `view` permission) login user
				mediator.viewer(self, None)
				# # be editor (has `view`, `change`) login user
				# mediator.editor(self, None)
				# be viewer anonymous user
				mediator.viewer(self, 'anonymous')
			elif self.pub_state == 'protected':
				mediator.viewer(self, None)
				# reject anonymous user
				mediator.reject(self, 'anonymous')
			else:
				mediator.reject(self, None)
				mediator.reject(self, 'anonymous')

		# The method below is called every after when object ManyToMany relation is updated
		def modify_object_permission_m2m(self, mediator, sender, model, pk_set, removed):
			pass

``views.py``::

	from django.views.generic import list_detail
	from django.views.generic import create_update
	from object_permission.decorators import permission_required
	from models import Entry

	def object_list(request, *args, **kwargs):
		return list_detail.object_list(request, *args, **kwargs)

	@permission_required('blog.view_entry', Entry)
	def object_detail(request, object_id, *args, **kwargs):
		return list_detail.object_detail(request, object_id=object_id, *args, **kwargs)

	# actually `blog.add_entry` permission is not object permission
	# so you have to set permission to each user in Django's admin site or whatever
	@permission_required('blog.entry_add')
	def create_object(request, *args, **kwargs):
		return create_update.create_object(request, *args, **kwargs)
	
	@permission_required('blog.change_entry', Entry)
	def update_object(request, object_id, *args, **kwargs):
		return create_update.update_object(request, object_id=object_id, *args, **kwargs)

	@permission_required('blog.delete_entry', Entry)
	def delete_object(request, object_id, *args, **kwargs):
		return create_update.delete_object(request, object_id=object_id, *args, **kwargs)

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
``OBJECT_PERMISSION_MODIFY_FUNCTION``
    set the name of function when object is saved for modify object permission for the object.
    the default value is ``modify_object_permission``

``OBJECT_PERMISSION_MODIFY_M2M_FUNCTION``
    set the name of function when object's ManyToMany relation is updated for modify object permission
    for the object. the default value is ``modify_object_permission_m2m``
