from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from CardNotificationConsumer import CardNotificationConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/cards/', CardNotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
