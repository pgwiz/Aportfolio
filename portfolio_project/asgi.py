# portfolio_project/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
application = get_default_application()