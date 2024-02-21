import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        print('*'*40)
        print('ChatConsumer connect - Подключение к комнате')
        print('self.scope     ------>', self.scope)
        print('room_name      ------>', self.room_name)
        print('room_group_name------>', self.room_group_name)
        print('channel_name   ------>', self.channel_name)
        print('*'*40, '\n')

        # Подключение к комнате
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключение от комнаты

        print('*'*40)
        print('ChatConsumer disconnect - Отключение от комнаты')
        print('room_name      ------>', self.room_name)
        print('room_group_name------>', self.room_group_name)
        print('channel_name   ------>', self.channel_name)
        print('*'*40)
        print()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        aaa = {}
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username
        type_mes = text_data_json['type_mes']

        print('*'*40)
        print('ChatConsumer receive - Отправка сообщения в комнату')
        print('text_data     ------>', text_data)
        print('text_data_json------>', text_data_json)
        print('*'*40, '\n')

        # Отправка сообщения в комнату
        await self.channel_layer.group_send(

            self.room_group_name,
            {
                'type': 'chat.message',
                'type_mes': type_mes,
                'message': message,
                'username': username,
                # 'what': '',
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения обратно на клиент
        print('+'*40)
        print('ChatConsumer chat_message - Отправка сообщения обратно на клиент')
        print('event------->\n', event)
        print('+'*40, '\n')

        type_mes = event['type_mes']
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type_mes': type_mes,
            'message': message,
            'username': username,
        }))
