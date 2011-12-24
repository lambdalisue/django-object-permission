#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
TestCase module for testing App

Original code is found at
http://stackoverflow.com/questions/502916/django-how-to-create-a-model-dynamically-just-for-testing
"""
import copy

from django.conf import settings
from django.core.management import call_command
from django.db.models import loading
from django import test

class AppTestCase(test.TestCase):
    installed_apps = []

    def _get_installed_apps(self):
        _installed_apps = list(settings.INSTALLED_APPS)
        for app in self.installed_apps:
            if app not in _installed_apps:
                _installed_apps.append(app)
        return _installed_apps

    def _pre_setup(self):
        # store original installed apps
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        # get extra required apps
        settings.INSTALLED_APPS = self._get_installed_apps()
        # Call syncdb to create db for extra apps (migrate=False for South)
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0, migrate=False)
        # Call the original method that does the fixtures etc.
        super(AppTestCase, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method
        super(AppTestCase, self)._post_teardown()
        # Restore the settings
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False
