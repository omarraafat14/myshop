"""
import the celery module to ensure it is loaded when Django starts.
"""

# import celery
from .celery import app as celery_app

__all__ = ["celery_app"]
