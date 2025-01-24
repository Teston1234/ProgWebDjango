import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from membre.models import Salon, Message  # Import statique des modèles

class SalonConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.salon_id = self.scope['url_route']['kwargs']['salon_id']
        self.salon_group_name = f'salon_{self.salon_id}'

        await self.channel_layer.group_add(
            self.salon_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.salon_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Message reçu : {text_data}")
        data = json.loads(text_data)
        message_content = data['message']
        user = self.scope['user']

        # Sauvegarder le message
        salon = await sync_to_async(Salon.objects.get, thread_sensitive=True)(id=self.salon_id)
        message = await sync_to_async(Message.objects.create, thread_sensitive=True)(
            salon=salon,
            user=user,
            contenu=message_content,
        )

        # Envoyer le message à tous les membres du groupe
        await self.channel_layer.group_send(
            self.salon_group_name,
            {
                'type': 'chat_message',
                'message': message.contenu,
                'user': user.username,
                'date': str(message.date_creation),
            }
        )

    async def chat_message(self, event):
        # Diffuser le message à la WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'date': event['date'],
        }))
