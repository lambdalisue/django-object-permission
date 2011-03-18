# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.conf import settings
from django.db.models.loading import get_models
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured

from ...mediators import ObjectPermissionMediator

class Command(BaseCommand):
    help = u"Remodify object_permission of each model using model's `modify_object_permission(self, mediator, created)` function."

    def handle(self, *app_labels, **options):
        # Historyを停止
        settings.HISTORY_ENABLE = False
        from django.db import models
        if not app_labels:
            output = [self.handle_noargs(**options)]
        else:
            try:
                app_list = [models.get_app(app_label) for app_label in app_labels]
            except (ImproperlyConfigured, ImportError), e:
                raise CommandError("%s. Are you sure your INSTALLED_APPS setting is correct?" % e)
            output = []
            for app in app_list:
                app_output = self.handle_app(app, **options)
                if app_output:
                    output.append(app_output)
        # Historyを再開
        settings.HISTORY_ENABLE = True
        return '\n'.join(output)
    
    def handle_app(self, app, **options):
        u"Remodify object_permission of each model using model's `modify_object_permission(self, mediator, created)` function."
        output = []
        model_list = get_models(app)
        for model in model_list:
            _output = self._remodify_object_permission(model, **options)
            if _output:
                output.append(_output)
        return "\n".join(output)
    
    def handle_noargs(self, **options):
        output = []
        content_types = ContentType.objects.all()
        for ct in content_types:
            model = ct.model_class()
            _output = self._remodify_object_permission(model, **options)
            if _output:
                output.append(_output)
        return "\n".join(output)
    
    def _remodify_object_permission(self, model, **options):
        NAME = settings.OBJECT_PERMISSION_MODIFY_FUNCTION
        NAME_M2M = settings.OBJECT_PERMISSION_MODIFY_M2M_FUNCTION
        output = []
        if not hasattr(model, NAME) and not hasattr(model, NAME_M2M):
            if options['verbosity'] == '2':
                output.append("Skipped: %s doesn't have `%s` and `%s` function." % (model, NAME, NAME_M2M))
        else:
            has = hasattr(model, NAME)
            has_m2m = hasattr(model, NAME_M2M)
            count = model.objects.count()
            for obj in model.objects.all():
                if has:
                    fn = getattr(obj, NAME)
                    fn(mediator=ObjectPermissionMediator, created=False)
                if has_m2m:
                    fn_m2m = getattr(obj, NAME_M2M)
                    for field in obj._meta.many_to_many:
                        sender = field.rel.through
                        model = field.rel.to
                        pk_set = [to.pk for to in getattr(obj, field.attname).all()]
                        fn_m2m(mediator=ObjectPermissionMediator, sender=sender, model=model, pk_set=pk_set, removed=False)
            if options['verbosity'] != '0':
                output.append("Modified: %s's object_permission has remodified (%d)" % (model, count))
        return "\n".join(output)