# notifications/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def notify_bug_created(project_id, bug_data, assigned_user_id=None, project_owner_id=None):
    channel_layer = get_channel_layer()
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
    # Notify assigned user directly if exists
    if assigned_user_id:
        async_to_sync(channel_layer.group_send)(
            f'user_{assigned_user_id}',
            {
                'type': 'bug_assigned',
                'data': {
                    'event': 'bug_assigned',
                    'bug': bug_data
                }
            }
        )
    if project_owner_id:
        async_to_sync(channel_layer.group_send)(
            f'user_{project_owner_id}',
            {
                'type': 'bug_created',
                'data': {
                    'event': 'bug_created',
                    'bug': bug_data
                }
            }
        )
    
def notify_bug_updated(project_id, bug_data, assigned_user_id=None, project_owner_id=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',  # this becomes asgi:group:project_1
        {
            'type': 'bug_updated',
            'data': {
                'event': 'bug_updated',
                'bug': bug_data
            }
        }
    )
    # Notify assigned user directly if exists
    if assigned_user_id:
        async_to_sync(channel_layer.group_send)(
            f'user_{assigned_user_id}',
            {
                'type': 'bug_assigned',
                'data': {
                    'event': 'bug_assigned',
                    'bug': bug_data
                }
            }
        )
    if project_owner_id:
        async_to_sync(channel_layer.group_send)(
            f'user_{project_owner_id}',
            {
                'type': 'bug_updated',
                'data': {
                    'event': 'bug_updated',
                    'bug': bug_data
                }
            }
        )

def notify_bug_closed(project_id, bug_data, assigned_user_id=None, project_owner_id=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',  # this becomes asgi:group:project_1
        {
            'type': 'bug_closed',
            'data': {
                'event': 'bug_closed',
                'bug': bug_data
            }
        }
    )
    # Notify assigned user directly if exists
    if assigned_user_id:
        async_to_sync(channel_layer.group_send)(
            f'user_{assigned_user_id}',
            {
                'type': 'bug_assigned',
                'data': {
                    'event': 'bug_assigned',
                    'bug': bug_data
                }
            }
        )
    if project_owner_id:
        async_to_sync(channel_layer.group_send)(
            f'user_{project_owner_id}',
            {
                'type': 'bug_closed',
                'data': {
                    'event': 'bug_closed',
                    'bug': bug_data
                }
            }
        )