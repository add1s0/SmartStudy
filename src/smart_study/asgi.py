"""ASGI config for Smart Study AI."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_study.settings")

application = get_asgi_application()
