# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bugs/(?P<project_id>\d+)/$', consumers.BugCreatedConsumer.as_asgi()),
    re_path(r"ws/comments/(?P<user_id>\d+)/$", consumers.CommentNotificationConsumer.as_asgi()),

]
