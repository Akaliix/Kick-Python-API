import httpx
import time
import threading

KICK_OAUTH_URL = "https://id.kick.com/oauth"
KICK_API_URL = "https://api.kick.com/public/v1"

class KickAPI:
    def __init__(self, client_id, client_secret, redirect_uri=None, code=None, code_verifier=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code = code
        self.code_verifier = code_verifier
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0
        self.lock = threading.Lock()
        self._start_auto_refresh()

    def _start_auto_refresh(self):
        t = threading.Thread(target=self._auto_refresh, daemon=True)
        t.start()

    def _auto_refresh(self):
        while True:
            if self.access_token and time.time() > self.token_expiry - 60:
                try:
                    self.refresh_access_token()
                except Exception as e:
                    print("Token refresh failed:", e)
            time.sleep(30)

    def get_app_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        resp = httpx.post(f"{KICK_OAUTH_URL}/token", data=data)
        resp.raise_for_status()
        tokens = resp.json()
        self.access_token = tokens["access_token"]
        self.token_expiry = time.time() + tokens["expires_in"]
        return self.access_token

    def get_user_access_token(self):
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier,
            "code": self.code,
        }
        resp = httpx.post(f"{KICK_OAUTH_URL}/token", data=data)
        resp.raise_for_status()
        tokens = resp.json()
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.token_expiry = time.time() + tokens["expires_in"]
        return tokens

    def refresh_access_token(self):
        if not self.refresh_token:
            return self.get_app_access_token()
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
        resp = httpx.post(f"{KICK_OAUTH_URL}/token", data=data)
        resp.raise_for_status()
        tokens = resp.json()
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.token_expiry = time.time() + tokens["expires_in"]
        return tokens

    def api_get(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = httpx.get(f"{KICK_API_URL}{endpoint}", params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def api_post(self, endpoint, data=None):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = httpx.post(f"{KICK_API_URL}{endpoint}", json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()