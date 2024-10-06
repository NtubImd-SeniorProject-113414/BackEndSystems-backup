import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from BackEndSystem import settings
from backendApp.models import Order, Patient
from asgiref.sync import sync_to_async


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

class OrderArrivedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('order_arrived_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('order_arrived_group', self.channel_name)

    async def receive(self, text_data=None):
        if text_data:
            data = json.loads(text_data)

            payload = data.get('payload', '').split(",")
            patient_id, order_id = payload[0], payload[1]

            order = await sync_to_async(Order.objects.filter(order_id=order_id).first)()
            patient = await sync_to_async(Patient.objects.filter(patient_id=patient_id).first)()

            if order and patient:
                DEFAULT_IMAGE_PATH = os.path.join(settings.STATIC_URL, 'img', 'patient_default_image.png')
                course = await sync_to_async(lambda: order.course)()
                course_name = await sync_to_async(lambda: course.course_name)()
                course_image_path = await sync_to_async(lambda: course.course_image.url if course.course_image else None)()
                patient_name = await sync_to_async(lambda: patient.patient_name)()
                patient_image_path = await sync_to_async(lambda: patient.patient_image_path.url if patient.patient_image_path else DEFAULT_IMAGE_PATH)()

                await self.channel_layer.group_send(
                    'order_arrived_group',
                    {
                        'type': 'order_message', 
                        'course_name': course_name,
                        'course_image_path': course_image_path,
                        'patient_name': patient_name,
                        'patient_image_path': patient_image_path
                    }
                )

    async def order_message(self, event):
        course_name = event['course_name']
        course_image_path = event['course_image_path']
        patient_name = event['patient_name']
        patient_image_path = event['patient_image_path']

        await self.send(text_data=json.dumps({
            'course_name': course_name,
            'course_image_path': course_image_path,
            'patient_name': patient_name,
            'patient_image_path': patient_image_path
        }))