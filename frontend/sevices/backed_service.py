import requests


class BackendService:
    BASE_URL = "http://127.0.0.1:8000"  # Replace with your FastAPI URL

    @staticmethod
    def get_users():
        response = requests.get(f"{BackendService.BASE_URL}/users")
        return response.json()

    @staticmethod
    def add_user(user_data):
        response = requests.post(f"{BackendService.BASE_URL}/users", json=user_data)
        return response.json()
