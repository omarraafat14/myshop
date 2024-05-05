import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")

# create an instance of the application
app = Celery("myshop")

# load any custom configuration from your project settings,
# The namespace attribute specifies the prefix that Celery-related settings will have in
# settings.py file. By setting the CELERY namespace, all Celery settings need to include
# the CELERY_ prefix in their name (for example, CELERY_BROKER_URL).
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover asynchronous tasks for your applications.
# Celery will look for a tasks.py file in each application.
app.autodiscover_tasks()
