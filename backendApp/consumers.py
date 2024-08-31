import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('image_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('image_group', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            await self.channel_layer.group_send(
                'image_group',
                {
                    'type': 'send_image',
                    'bytes_data': bytes_data
                }
            )

    async def send_image(self, event):
        bytes_data = event['bytes_data']
        await self.send(bytes_data=bytes_data)
