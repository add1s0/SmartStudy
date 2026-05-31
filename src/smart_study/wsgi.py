"""WSGI config for Smart Study AI."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_study.settings")

application = get_wsgi_application()
