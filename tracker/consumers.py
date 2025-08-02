# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BugCreatedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f'project_{self.project_id}'
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def bug_created(self, event):
        await self.send(text_data=json.dumps(event['data']))
        
    async def bug_updated(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def bug_closed(self, event):
        await self.send(text_data=json.dumps(event['data']))

class CommentNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{self.user_id}'

        # Allow all connections (no auth)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_comment_notification(self, event):
        await self.send(text_data=json.dumps(event['data']))
