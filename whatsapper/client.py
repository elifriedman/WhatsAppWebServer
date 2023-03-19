import requests

class WhatsappAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session_id = None
    
    def open_browser(self):
        url = f"{self.base_url}/open"
        response = requests.get(url)
        json = response.json()
        if "session_id" in json:
            self.session_id = json["session_id"]
            return True
        return response.json()

    def sessions(self):
        url = f"{self.base_url}/sessions"
        response = requests.get(url)
        json = response.json()
        return [row['session_id'] for row in json]

    def number(self, phone, message=None, session_id=None):
        if session_id is None:
            session_id = self.session_id
        url = f"{self.base_url}/number"
        params = {"session_id": session_id}
        params["phone"] = phone
        if message:
            params["message"] = message
        response = requests.get(url, params=params)
        return response.json()

    def write(self, message, send=False, session_id=None):
        if session_id is None:
            session_id = self.session_id
        url = f"{self.base_url}/write"
        params = {"session_id": session_id}
        params["message"] = message
        if send:
            params["send"] = True
        response = requests.get(url, params=params)
        return response.json()

    def send(self, session_id=None):
        if session_id is None:
            session_id = self.session_id
        url = f"{self.base_url}/send"
        params = {"session_id": session_id}
        response = requests.get(url, params=params)
        return response.json()

    def close_browser(self, session_id=None):
        if session_id is None:
            session_id = self.session_id
        params = {"session_id": session_id}
        url = f"{self.base_url}/close"
        response = requests.get(url, params=params)
        return response.json()

