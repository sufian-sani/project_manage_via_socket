import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async


class ProjectNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']

        # Parse user_id from query string
        query_string = parse_qs(self.scope["query_string"].decode())
        self.user_id = query_string.get("user_id", [None])[0]
        
        from django.contrib.auth import get_user_model
        from tracker.models import Project, Bug

        User = get_user_model()

        if not self.user_id:
            await self.close()
            return

        try:
            user = await sync_to_async(User.objects.get)(id=self.user_id)
            project = await sync_to_async(Project.objects.get)(id=self.project_id)
            # bug = await sync_to_async(Bug.objects.filter)(project=project)
            # bug = await sync_to_async(Bug.objects.filter)(project=project, assigned_to=user)
            # Allow if user is owner or has assigned bugs in this project
            is_owner = project.owner_id == user.id
            is_assigned = await sync_to_async(Bug.objects.filter(project=project, assigned_to=user).exists)()

            if not (is_owner or is_assigned):
                await self.close()
                return

        except (User.DoesNotExist, Project.DoesNotExist):
            await self.close()
            return
        
        # Allow only if the user is the project owner
        # breakpoint()  # For debugging purposes, can be removed later

        self.room_group_name = f'project_{self.project_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Optional: process messages sent from frontend
        pass

    async def bug_created(self, event):
        # breakpoint()  # For debugging purposes, can be removed later
        if str(self.project_id) == str(event['data']['bug']['project']):
            await self.send(text_data=json.dumps(event['data']))
            
    async def bug_assigned(self, event):
        if str(self.project_id) == str(event['data']['bug']['project']):
            await self.send(text_data=json.dumps(event['data']))
            
    async def bug_updated(self, event):
        if str(self.project_id) == str(event['data']['bug']['project']):
            await self.send(text_data=json.dumps(event['data']))
        
    async def bug_closed(self, event):
        if str(self.project_id) == str(event['data']['bug']['project']):
            await self.send(text_data=json.dumps(event['data']))

# # consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from urllib.parse import parse_qs
# from asgiref.sync import sync_to_async



# class ProjectNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.project_id = self.scope['url_route']['kwargs']['project_id']
#         self.user_id = self.scope['query_string'].decode().split('=')[1]
#         self.user = await sync_to_async(User.objects.get)(id=user_id)

#         # 💡 Import inside the method — ensures Django is ready
#         from django.contrib.auth import get_user_model
#         from tracker.models import Project

#         User = get_user_model()

#         try:
#             project = await database_sync_to_async(Project.objects.get)(id=self.project_id)
#             user = await database_sync_to_async(User.objects.get)(id=self.user_id)

#             if not await self.is_user_in_project(user, project):
#                 await self.close()
#                 return

#         except Project.DoesNotExist:
#             await self.close()
#             return

#         self.room_group_name = f'project_{self.project_id}'
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         # process incoming message
#         pass

#     async def is_user_in_project(self, user, project):
#         if project.owner != user:
#             return False
#         return True
    
#     async def bug_created(self, event):
#         await self.send(text_data=json.dumps(event['data']))
    
    
    
    # async def connect(self):
    #     self.project_id = self.scope['url_route']['kwargs']['project_id']
    #     # self.group_name = f'project_{self.project_id}'
        
    #     # Parse user_id from query string
    #     query_string = self.scope["query_string"].decode()
    #     user_id = parse_qs(query_string).get("user_id", [None])[0]
        
    #     # Check if project exists and user is associated
    #     try:
    #         project = await self.get_project(self.project_id)
    #         user = await self.get_user(user_id)

    #         if user and await self.is_user_associated(project, user):
    #             await self.channel_layer.group_add(
    #                 self.group_name,
    #                 self.channel_name
    #             )
    #             await self.accept()
    #         else:
    #             await self.close(code=403)
    #     except Exception as e:
    #         print(f"WebSocket auth error: {e}")
    #         await self.close(code=403)

    #     # Join group
    #     await self.channel_layer.group_add(
    #         self.group_name,
    #         self.channel_name
    #     )
    #     await self.accept()

    # async def disconnect(self, close_code):
    #     # Leave group
    #     await self.channel_layer.group_discard(
    #         self.group_name,
    #         self.channel_name
    #     )
        
    # # ----------------------
    
    # async def bug_created(self, event):
    #     await self.send(text_data=json.dumps(event['data']))
    
    # # ----------------------
        
    # @database_sync_to_async
    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         return None

    # @database_sync_to_async
    # def get_project(self, project_id):
    #     return Project.objects.get(id=project_id)
    
    # @database_sync_to_async
    # def is_user_associated(self, project, user):
    #     # Update this depending on your Project model
    #     return user == project.owner

    # async def receive(self, text_data):
    #     # Optionally handle incoming messages
    #     pass

    # async def bug_created(self, event):
    #     await self.send(text_data=json.dumps(event['data']))
        
        
# class BugConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get user_id from query params
#         query_string = self.scope.get("query_string", b"").decode()
#         from urllib.parse import parse_qs
#         params = parse_qs(query_string)
#         user_ids = params.get("user_id")
#         # breakpoint()
        
#         if not user_ids:
#             await self.close()  # No user_id provided, reject connection
#             return
        
#         self.user_id = user_ids[0]
#         self.group_name = f"user_{self.user_id}"

#         # Join group for this user id
#         print(f"Connecting to group: {self.group_name}")
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def bug_assigned(self, event):
#         await self.send(text_data=json.dumps(event['data']))
        
#     async def bug_created(self, event):
#         await self.send(text_data=json.dumps(event['data']))
        
#     async def bug_updated(self, event):
#         await self.send(text_data=json.dumps(event['data']))
        
#     async def bug_closed(self, event):
#         await self.send(text_data=json.dumps(event['data']))
    
    
#     # async def connect(self):
#     #     user = self.scope["user"]
#     #     self.user_id = getattr(user, 'id', None)
#     #     self.group_name = f"user_{self.user_id}" if self.user_id else None

#     #     if user.is_anonymous:
#     #         await self.close()
#     #     else:
#     #         await self.channel_layer.group_add(
#     #             self.group_name,
#     #             self.channel_name
#     #         )
#     #         await self.accept()

#     # async def disconnect(self, close_code):
#     #     if self.group_name:
#     #         await self.channel_layer.group_discard(
#     #             self.group_name,
#     #             self.channel_name
#     #         )

#     # async def receive(self, text_data):
#     #     # You can process incoming messages here if needed
#     #     pass

#     # async def bug_assigned(self, event):
#     #     await self.send(text_data=json.dumps(event['data']))

#     # async def bug_created(self, event):
#     #     await self.send(text_data=json.dumps(event['data']))

# # ----for public bugs----
# class PublicBugConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = "public_bugs"

#         # Join the group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def bug_created(self, event):
#         # Send the bug notification to the WebSocket client
#         await self.send(text_data=json.dumps(event["data"]))

# # ------------------------------start of comment consumer------------------------------
# class CommentNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user_id = self.scope['url_route']['kwargs']['user_id']
#         self.group_name = f'user_{self.user_id}'

#         # Allow all connections (no auth)
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def send_comment_notification(self, event):
#         await self.send(text_data=json.dumps(event['data']))
