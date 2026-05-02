"""
ASGI config for portfolio_project.

Exposes the ASGI callable as a module-level variable named ``application``.
HTTP traffic is routed through the standard Django ASGI app, while
WebSocket traffic is routed through Channels using the URL patterns
declared in ``chat.routing.websocket_urls``.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings")

# Initialise Django before importing any code that may touch the ORM /
# settings (e.g. consumers). ``get_asgi_application()`` triggers
# ``django.setup()``.
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402

from chat.routing.websocket_urls import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
