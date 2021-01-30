import json
from channels.generic.websocket import AsyncWebsocketConsumer
from queues.models import Live_Queue

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue_id = self.scope['url_route']['kwargs']['queue_id']
        self.queue_group_name = 'queue_%s' % self.queue_id

        await self.channel_layer.group_add(
            self.queue_group_name,
            self.channel_name
        )
        await self.accept()

        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.queue_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        number = text_data_json['number']

        await self.channel_layer.group_send(
            self.queue_group_name,
            {
                'type': 'message',
                'number': number,
            }
        )    

    async def message(self, event):
        message = event['number']
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    pass
