"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa
# Explicit imports to suppress flake8 errors.
from .base import DATABASES, INSTALLED_APPS, MIDDLEWARE, TEMPLATES, env

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# DATABASES['tpj'] = {
#     'NAME': env('TPJ_DB_NAME'),
#     'ENGINE': env('TPJ_DB_ENGINE'),
#     'HOST': env('TPJ_DB_HOST'),
#     'PORT': env('TPJ_DB_PORT'),
#     'USER': env('TPJ_DB_USER'),
#     'PASSWORD': env('TPJ_DB_PASSWORD'),
#     'OPTIONS': {
#         'driver': 'FreeTDS',
#         'unicode_results': True,
#         'host_is_server': True,
#         'extra_params': 'tds_version=9.1',
#     }
# }
# DATABASE_ROUTERS = ['influencetx.tpj.routers.DatabaseRouter']
TPJ_MANAGED = True

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='O~TBa::OFqYvU**7&unz~UVP7[ACpr7aV^x8he5Kp/``s_Vuh.')

# Mail settings
# ------------------------------------------------------------------------------
#
#EMAIL_PORT = 1025
#
#EMAIL_HOST = 'localhost'
#EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
#                    default='django.core.mail.backends.console.EmailBackend')
#

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['localhost', '127.0.0.1', '10.0.2.2', ]

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '*.influencetx.com'])
