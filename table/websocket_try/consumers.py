import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync  

class TestConsumer(WebsocketConsumer):
    def connect(self):
        print('COME TO MAKE DEALS')
        self.accept()

    def receive(self, text_data):

        self.room_group_name = str(self.scope['user'].id)  # Имя группы базируется на идентификаторе пользователя
        async_to_sync(self.channel_layer.group_add)(
            str(self.room_group_name),
            self.channel_name
        )

        data_to_frontend = json.dumps(
            {
                "event": "huy",
                "data": "IDI NAHUY"
            }
        )
        self.send(data_to_frontend)

    def events_alarm(self, event):
        print('come to huepizda')
        print(event)
        message = event.get('message', '')  # Получаем 'message' из event или используем пустую строку, если 'message' отсутствует
        data_to_frontend = json.dumps(
            {
                "event": "PIZDA",
                "data": message
            }
        )

        self.send(data_to_frontend)

    def disconnect(self, code):
        print("server says disconnected")
