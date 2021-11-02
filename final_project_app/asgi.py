"""
ASGI config for final_project_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import get_default_application

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project_app.settings')
django.setup()
application = get_default_application()
