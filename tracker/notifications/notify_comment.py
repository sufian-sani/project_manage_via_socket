# in your notifications.py or utils
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user_comment(id, comment_data):
    channel_layer = get_channel_layer()
    # breakpoint()  # For debugging purposes, can be removed later
    async_to_sync(channel_layer.group_send)(
        f"user_{id}",
        {
            "type": "send.comment.notification",
            "data": {
                "event": "comment_notification",
                "comment": comment_data
            }
        }
    )
