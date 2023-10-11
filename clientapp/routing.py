# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/cam", consumers.CamConsumer.as_asgi()),
    re_path(r"ws/loading", consumers.LoadingConsumer.as_asgi()),
]