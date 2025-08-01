# listen_redis.py
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# This is the internal key Django Channels uses for group messages
# Warning: Channels uses message encoding, so it may not be fully human-readable.
channel_name = 'asgi:group:project_1'

pubsub = r.pubsub()
pubsub.subscribe(channel_name)

print(f"🔌 Subscribed to {channel_name}... Waiting for messages.")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"\n📨 Message received:\n{message['data']}")
