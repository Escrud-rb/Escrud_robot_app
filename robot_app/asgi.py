
import os

from django.core.asgi import get_asgi_application

from django.conf import settings

# settings.configure()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "robot_app.settings")
django_asgi_app = get_asgi_application()

import main.routing
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    )
})
