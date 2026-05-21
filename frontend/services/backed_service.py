import requests
from os import getenv
AUTH_TOKEN = "your_jwt_token_here"  # Replace with the user's JWT token
BACKEND_HOST = getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = getenv("BACKEND_PORT", "9000")
BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

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
    def fetch_projects():
        """
        Fetch all projects from the backend.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        try:
            response = requests.get(f"{BASE_URL}/api/v1/projects", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching projects: {e}")
            return []

    @staticmethod
    def list_shots(project_id=None):
        """
        Fetch shots from the backend, optionally filtered by project.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }

        params = {}
        if project_id is not None:
            params["project_id"] = project_id

        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/shots",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching shots: {e}")
            return []

    @staticmethod
    def fetch_assets(project_id=None):
        """
        Fetch assets from the backend, optionally filtered by project.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }

        params = {}
        if project_id is not None:
            params["project_id"] = project_id

        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/assets",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching assets: {e}")
            return []
