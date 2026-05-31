"""ASGI config for Smart Study AI."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_study_ai.settings")

application = get_asgi_application()
