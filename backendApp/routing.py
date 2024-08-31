from django.urls import path
from . import consumers

# 定義 WebSocket 路徑
websocket_urlpatterns = [
    path('ws/image/', consumers.ImageConsumer.as_asgi()),
]
