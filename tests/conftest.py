"""Pytest setup for the Django project."""
import os
import sys
from pathlib import Path

import django

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PROJECT_SRC))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_study_ai.settings")
django.setup()
