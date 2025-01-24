import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web2.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from Web2.routing import websocket_urlpatterns  # Assure-toi que le chemin est correct
# Initialisation de Django avant de définir l'application ASGI
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
