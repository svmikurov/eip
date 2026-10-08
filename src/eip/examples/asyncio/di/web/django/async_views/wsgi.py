"""WSGI config for async_views project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_views.settings')

application = get_wsgi_application()
