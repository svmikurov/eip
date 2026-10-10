"""ASGI config for async_views project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_views.settings')

application = get_asgi_application()
