import requests
# API by Void or VoidBox.alhasubji.store #
class VoidBoxAPI:
    def __init__(self, token: str = None, base_url: str = "https://voidbox.alhasubji.store"):
        self.token = token
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _handle_response(self, response):
        if response.status_code == 200:
            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    return response.json()
                except ValueError:
                    raise Exception(f"Error: Failed to parse JSON response. Status Code: {response.status_code}")
            else:
                print(f"Warning: Expected JSON response but got {response.headers.get('Content-Type')}. Status Code: {response.status_code}")
                print(response.text)
                return None
        else:
            raise Exception(f"Error: Received status code {response.status_code}. Response: {response.text}")

    def list_boxes(self):
        url = f"{self.base_url}/boxes"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def create_box(self, name: str, description: str):
        url = f"{self.base_url}/boxes"
        response = requests.post(url, headers=self.headers, json={"name": name, "description": description})
        return self._handle_response(response)

    def get_box(self, box_id: str):
        url = f"{self.base_url}/boxes/{box_id}"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def update_box(self, box_id: str, name: str, description: str):
        url = f"{self.base_url}/boxes/{box_id}"
        response = requests.put(url, headers=self.headers, json={"name": name, "description": description})
        return self._handle_response(response)

    def delete_box(self, box_id: str):
        url = f"{self.base_url}/boxes/{box_id}"
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    def upload_file(self, box_id: str, file_path: str):
        url = f"{self.base_url}/boxes/{box_id}/upload"
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(url, headers=self.headers, files=files)
            return self._handle_response(response)

    def stream_media(self, box_id: str, media_id: str):
        url = f"{self.base_url}/media/{box_id}/{media_id}/stream"
        response = requests.get(url, headers=self.headers, stream=True)
        return response


class Create:
    def __init__(self, base_url: str = "https://voidbox.alhasubji.store"):
        self.base_url = base_url

    def signup(self, username: str, password: str):
        url = f"{self.base_url}/signup"
        response = requests.post(url, json={"username": username, "password": password})
        return self._handle_response(response)

    def login(self, username: str, password: str):
        url = f"{self.base_url}/login"
        response = requests.post(url, json={"username": username, "password": password})
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    return response.json()
                except ValueError:
                    raise Exception(f"Error: Failed to parse JSON response. Status Code: {response.status_code}")
            else:
                print(f"Warning: Expected JSON response but got {response.headers.get('Content-Type')}. Status Code: {response.status_code}")
                print(response.text)
                return None
        else:
            raise Exception(f"Error: Received status code {response.status_code}.")