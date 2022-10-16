import imp
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync



class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("websocket connected...", event)
        print("channel layer", self.channel_layer)
        print("channel name", self.channel_name)
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(
            self.groupname, self.channel_name
            )

        self.send({
            'type':'websocket.accept',
        })

    def websocket_receive(self, event):
        print("message received from client...", event)
        async_to_sync(self.channel_layer.group_send)(
            self.groupname, {
            'type': 'chat.message',
            'message': event['text']
        })

    def websocket_disconnect(self, event):
        print("websocket disconnected", event)
        print("channel layer", self.channel_layer)
        print("channel name", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.groupname,
             self.channel_name
            )
        raise StopConsumer()

    def chat_message(self, event):
        print('Event...', event['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })




class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket connected...", event)
        print("channel layer", self.channel_layer)
        print("channel name", self.channel_name)
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        await self.channel_layer.group_add(
            self.groupname, self.channel_name
            )

        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self, event):
        print("message received from client...", event)
        await self.channel_layer.group_send(
            self.groupname, {
            'type': 'chat.message',
            'message': event['text']
        })

    async def websocket_disconnect(self, event):
        print("websocket disconnected", event)
        print("channel layer", self.channel_layer)
        print("channel name", self.channel_name)
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
            )
        raise StopConsumer()

    async def chat_message(self, event):
        print('Event...', event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })