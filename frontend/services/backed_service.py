import requests
from os import getenv
AUTH_TOKEN = "your_jwt_token_here"  # Replace with the user's JWT token
BACKEND_PORT = getenv("BACKEND_PORT", "9000")
BASE_URL = f"http://127.0.0.1:{BACKEND_PORT}"

class BackendService:

    @staticmethod
    def get_users():
        response = requests.get(f"{BackendService.BASE_URL}/users")
        return response.json()

    @staticmethod
    def add_user(user_data):
        response = requests.post(f"{BackendService.BASE_URL}/users", json=user_data)
        return response.json()

    @staticmethod
    def list_shots():
        """
        Fetch all shots from the backend.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"  # Authentication
        }
        try:
            response = requests.get(f"{BASE_URL}/api/v1/shots", headers=headers)  # Update the endpoint based on API
            response.raise_for_status()  # Raise HTTPError for bad HTTP responses
            data = response.json()
            return data  # Return fetched data
        except requests.RequestException as e:
            print(f"Error fetching shots: {e}")
            return []  # Return empty list on failure

    @staticmethod
    def fetch_assets():
        """
        Fetch hierarchical assets from the backend.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"  # Authentication
        }
        try:
            response = requests.get(f"{BASE_URL}/api/v1/assets", headers=headers)  # Update the endpoint based on API
            response.raise_for_status()  # Raise HTTPError for bad HTTP responses
            data = response.json()
            return data  # Return fetched data
        except requests.RequestException as e:
            print(f"Error fetching shots: {e}")
            return []  # Return empty list on failure
