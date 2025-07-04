from fastapi import FastAPI, Request, Header, HTTPException
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import httpx
import os
from kick_api import KickAPI

app = FastAPI()

# Load Kick public key (static or fetch from API)
KICK_PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq/+l1WnlRrGSolDMA+A8
6rAhMbQGmQ2SapVcGM3zq8ANXjnhDWocMqfWcTd95btDydITa10kDvHzw9WQOqp2
MZI7ZyrfzJuz5nhTPCiJwTwnEtWft7nV14BYRDHvlfqPUaZ+1KR4OCaO/wWIk/rQ
L/TjY0M70gse8rlBkbo2a8rKhu69RQTRsoaf4DVhDPEeSeI5jVrRDGAMGL3cGuyY
6CLKGdjVEM78g3JfYOvDU/RvfqD7L89TZ3iN94jrmWdGz34JNlEI5hqK8dd7C5EF
BEbZ5jgB8s8ReQV8H+MkuffjdAj3ajDDX3DOJMIut1lBrUVD1AaSrGCKHooWoL2e
twIDAQAB
-----END PUBLIC KEY-----"""

def verify_signature(message_id, timestamp, body, signature_b64):
    public_key = serialization.load_pem_public_key(KICK_PUBLIC_KEY)
    signed_data = f"{message_id}.{timestamp}.{body.decode()}".encode()
    signature = base64.b64decode(signature_b64)

    try:
        public_key.verify(
            signature,
            signed_data,  # Pass raw data, NOT pre-hashed
            padding.PKCS1v15(),
            hashes.SHA256()  # Let it hash internally
        )
        return True
    except Exception as e:
        print("Signature verification error:", e)
        return False

@app.post("/kick-webhook")
async def kick_webhook(
    request: Request,
    kick_event_message_id: str = Header(..., alias="kick-event-message-id"),
    kick_event_signature: str = Header(..., alias="kick-event-signature"),
    kick_event_message_timestamp: str = Header(..., alias="kick-event-message-timestamp"),
    kick_event_type: str = Header(..., alias="kick-event-type"),
):
    body = await request.body()
    #print("HEADERS:", dict(request.headers))
    
    if not verify_signature(kick_event_message_id, kick_event_message_timestamp, body, kick_event_signature):
        print("Invalid signature, skipping event handling")
        raise HTTPException(status_code=401, detail="Invalid signature")
    else:
        print("Signature verified successfully")
    
    event = await request.json()
    print(f"Received event: {kick_event_type}")
    print(event)
    # Add your event handling logic here
    return {"ok": True}