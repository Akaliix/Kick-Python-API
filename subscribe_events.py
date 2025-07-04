from kick_api import KickAPI
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_USER_ID = int(os.getenv("BROADCASTER_USER_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


kick = KickAPI(CLIENT_ID, CLIENT_SECRET)
kick.get_app_access_token()

# List of all event types you want to subscribe to
EVENTS = [
    {"name": "chat.message.sent", "version": 1},
    {"name": "channel.followed", "version": 1},
    {"name": "channel.subscription.renewal", "version": 1},
    {"name": "channel.subscription.gifts", "version": 1},
    {"name": "channel.subscription.new", "version": 1},
    {"name": "livestream.status.updated", "version": 1},
    {"name": "livestream.metadata.updated", "version": 1},
    {"name": "moderation.banned", "version": 1},
]

data = {
    "broadcaster_user_id": BROADCASTER_USER_ID,
    "events": EVENTS,
    "method": "webhook",
    "webhook_url": WEBHOOK_URL,
}
resp = kick.api_post("/events/subscriptions", data)
print("Subscribed:", resp)