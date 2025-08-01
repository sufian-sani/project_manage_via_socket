# in your notifications.py or utils
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_comment_added(bug, comment_data):
    channel_layer = get_channel_layer()

    recipients = set()

    if bug.created_by:
        recipients.add(f"user_{bug.created_by.id}")
    if bug.assigned_to:
        recipients.add(f"user_{bug.assigned_to.id}")

    for user_group in recipients:
        async_to_sync(channel_layer.group_send)(
            user_group,
            {
                "type": "comment.added",
                "data": {
                    "event": "comment_added",
                    "bug_id": bug.id,
                    "comment": comment_data
                }
            }
        )
