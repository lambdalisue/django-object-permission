import warnings
from django.conf import settings
if 'django.contrib.flatpages' not in settings.INSTALLED_APPS:
    warnings.warn('"django.contrib.flatpages" is required to run "django-object-permissions" test')
else:
    from test_models import *
    from test_permissions import *
