import requests

# Owner of API is Void or @sr_sr on telegram, Join his channel at https://t.me/TrProGram.
class VoidBoxAPI:
    def __init__(self, token: str, base_url: str = "https://voidbox.alhasubji.store"):
        self.token = token
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def signup(self, username: str, password: str):
        url = f"{self.base_url}/signup"
        return requests.post(url, json={"username": username, "password": password}).json()

    def login(self, username: str, password: str):
        url = f"{self.base_url}/login"
        return requests.post(url, json={"username": username, "password": password}).json()

    def get_me(self):
        url = f"{self.base_url}/getMe"
        return requests.get(url, headers=self.headers).json()

    def list_boxes(self):
        url = f"{self.base_url}/boxes"
        return requests.get(url, headers=self.headers).json()

    def create_box(self, name: str, description: str):
        url = f"{self.base_url}/boxes"
        return requests.post(url, headers=self.headers, json={"name": name, "description": description}).json()

    def get_box(self, box_id: str):
        url = f"{self.base_url}/boxes/{box_id}"
        return requests.get(url, headers=self.headers).json()

    def update_box(self, box_id: str, name: str, description: str):
        url = f"{self.base_url}/boxes/{box_id}"
        return requests.put(url, headers=self.headers, json={"name": name, "description": description}).json()

    def delete_box(self, box_id: str):
        url = f"{self.base_url}/boxes/{box_id}"
        return requests.delete(url, headers=self.headers).json()

    def upload_file(self, box_id: str, file_path: str):
        url = f"{self.base_url}/boxes/{box_id}/upload"
        with open(file_path, "rb") as file:
            files = {"file": file}
            return requests.post(url, headers=self.headers, files=files).json()

    def stream_media(self, box_id: str, media_id: str):
        url = f"{self.base_url}/media/{box_id}/{media_id}/stream"
        return requests.get(url, headers=self.headers, stream=True)