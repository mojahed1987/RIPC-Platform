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