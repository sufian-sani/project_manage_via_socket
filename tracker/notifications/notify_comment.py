# in your notifications.py or utils
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_project_comment(id, comment_data):
    channel_layer = get_channel_layer()
    # breakpoint()  # For debugging purposes, can be removed later
    async_to_sync(channel_layer.group_send)(
        f"project_{id}",
        {
            "type": "send_comment_notification",
            "data": {
                "event": "send_comment_notification",
                "project_id": id,
                "comment": comment_data
            }
        }
    )
