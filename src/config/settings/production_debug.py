"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa
# Explicit imports to suppress flake8 errors.
from .base import INSTALLED_APPS, MIDDLEWARE, TEMPLATES, env


INSTALLED_APPS += ['gunicorn', ]

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY')

# Mail settings
# ------------------------------------------------------------------------------

# EMAIL_PORT = 1025
# EMAIL_HOST = 'localhost'
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Static Assets
# ------------------------
STATIC_URL = 'https://static.influencetx.com/static/'

CORS_ORIGIN_WHITELIST = [
    '*.influencetx.com',
    'localhost',
    '*.influencetexas.com'
]

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '.influencetx.com', '.influencetexasx.com'])
