"""
Creates permissions for all installed apps that need permissions.
"""
from django.contrib.auth.management import _get_permission_codename
from django.db.models import get_models, signals
from django.contrib.auth import models as auth_app

def _get_all_permissions(opts):
    "Returns (codename, name) for all permissions in the given opts."
    perms = []
    for action in ('view',):
        perms.append((_get_permission_codename(action, opts), u'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms + list(opts.permissions)

def create_permissions(app, created_models, verbosity, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    app_models = get_models(app)
    if not app_models:
        return
    for klass in app_models:
        ctype = ContentType.objects.get_for_model(klass)
        for codename, name in _get_all_permissions(klass._meta):
            p, created = Permission.objects.get_or_create(codename=codename, content_type__pk=ctype.id,
                defaults={'name': name, 'content_type': ctype})
            if created and verbosity >= 2:
                print "Adding permission '%s'" % p

signals.post_syncdb.connect(create_permissions,
    dispatch_uid = "object_permission.management.create_permissions")