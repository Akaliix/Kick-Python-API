from kick_api import KickAPI
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_USER_ID = os.getenv("BROADCASTER_USER_ID")
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

if BROADCASTER_USER_ID is None:
    print("ERROR: BROADCASTER_USER_ID is not set. Please check your environment variables.")
    exit(1)

if WEBHOOK_URL is None:
    print("ERROR: WEBHOOK_URL is not set. Please check your environment variables.")
    exit(1)

data = {
    "broadcaster_user_id": int(BROADCASTER_USER_ID),  # Ensure integer type
    "events": EVENTS,
    "method": "webhook",
    "webhook_url": WEBHOOK_URL,
}

try:
    resp = kick.api_post("/events/subscriptions", data)
    print("Subscribed:", resp)
except Exception as e:
    import httpx
    if isinstance(e, httpx.HTTPStatusError):
        print("ERROR RESPONSE:", e.response.text)
    raise