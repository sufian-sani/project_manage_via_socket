# notifications/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_bug_created(project_id, bug_data):
    channel_layer = get_channel_layer()
    print(f"Notifying project {project_id} about new bug: {bug_data}")
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',  # this becomes asgi:group:project_1
        {
            'type': 'bug_created',
            'data': {
                'event': 'bug_created',
                'bug': bug_data
            }
        }
    )
    
def notify_bug_updated(project_id, bug_data):
    channel_layer = get_channel_layer()
    print(f"Notifying project {project_id} about updated bug: {bug_data}")
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': 'bug.updated',
            'data': {
                'event': 'bug_updated',
                'bug': bug_data
            }
        }
    )

def notify_bug_closed(project_id, bug_data):
    channel_layer = get_channel_layer()
    print(f"Notifying project {project_id} about closed bug: {bug_data}")
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': 'bug.closed',
            'data': {
                'event': 'bug_closed',
                'bug': bug_data
            }
        }
    )