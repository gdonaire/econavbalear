"""
WSGI config for amarres project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


# Add the app's directory to the PYTHONPATH                                     
sys.path.append('/home/vvidal/django_projects/amarres')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amarres.settings")

application = get_wsgi_application()
