from django.urls import re_path

from . import consumers
from .consumers import MainConsumer

websocket_urlpatterns = [
    re_path(r'ws/(?P<client>\w+)/main/$', MainConsumer.as_asgi()),
]
