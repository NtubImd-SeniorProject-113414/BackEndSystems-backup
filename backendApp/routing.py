from django.urls import path
from . import consumers

# 定義 WebSocket 路徑s
websocket_urlpatterns = [
    path('ws/image/', consumers.ImageConsumer.as_asgi()),
    path('ws/order_arrived/', consumers.OrderArrivedConsumer.as_asgi()),
    
]
