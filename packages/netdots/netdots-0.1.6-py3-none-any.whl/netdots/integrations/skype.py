import requests

class Skype:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = f"{base_url}/skype"

    def _headers(self):
        return {"x-api-key": self.api_key}

    def send_message(self, payload: dict):
        url = f"{self.base_url}/send_message"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()