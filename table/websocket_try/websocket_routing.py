from django.urls import re_path
from table.websocket_try.consumers import TestConsumer


websocket_urlpatterns = [
    re_path(r'ws/socket-server/', TestConsumer.as_asgi())
]
