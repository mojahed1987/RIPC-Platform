import requests

from core.config.settings import BASE_URL, TIMEOUT


class RIPCClient:

    def __init__(self, token):

        self.token = token

        self.headers = {
            "X-Authorization": f"Bearer {token}",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://es.ripc.gov.sa",
            "Referer": "https://es.ripc.gov.sa/ripc-main/"
        }

    def get(self, endpoint):

        url = f"{BASE_URL}{endpoint}"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=TIMEOUT
        )

        return response

    def post(self, endpoint, payload):

        url = f"{BASE_URL}{endpoint}"

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            timeout=TIMEOUT
        )

        return response

    def is_token_expired(self, response):

        if response.status_code in [401, 407]:
            return True

        try:
            data = response.json()
            msg = str(data).lower()

            if "login again" in msg:
                return True

            if "token" in msg and "expired" in msg:
                return True

            if "username and the password does not match" in msg:
                return True

        except Exception:
            pass

        return False