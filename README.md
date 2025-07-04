# Kick Python API Webhook Example

This project demonstrates how to use the Kick.com API to subscribe to events and receive webhooks using Python, FastAPI.

## Features
- Subscribe to Kick.com events (chat, follows, subscriptions, livestream, moderation, etc.)
- Receive and verify webhook events securely
- Example scripts for event subscription and webhook server

## Requirements
- Python 3.8+
- pip
- (Recommended) Linux or WSL

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Akaliix/Kick-Python-API.git
cd Kick-Python-API
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following:
```
CLIENT_ID=your_kick_client_id
CLIENT_SECRET=your_kick_client_secret
BROADCASTER_USER_ID=your_broadcaster_user_id
WEBHOOK_URL=https://your-server.com/kick-webhook
```

### 5. Run the Webhook Server
```bash
uvicorn webhook_server:app --host 0.0.0.0 --port 443
```

### 6. Subscribe to Events
```bash
python subscribe_events.py
```

## Files
- `kick_api.py` — Kick API wrapper
- `webhook_server.py` — FastAPI webhook receiver
- `subscribe_events.py` — Script to subscribe to events
- `requirements.txt` — Python dependencies
- `.env` — Your environment variables (not committed)

## License
MIT
