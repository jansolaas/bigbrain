import requests
from os import getenv

BACKEND_HOST = getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = getenv("BACKEND_PORT", "9000")
BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"


class BackendService:
    access_token = None
    current_user = None

    @classmethod
    def login(cls, username, password):
        """
        Log in with username/password, store the access token in memory,
        then fetch and store the current user.
        """
        payload = {
            "username": username,
            "password": password,
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            data=payload,
        )
        response.raise_for_status()

        data = response.json()
        cls.access_token = data.get("access_token")

        cls.current_user = cls.fetch_current_user()

        return data

    @classmethod
    def fetch_current_user(cls):
        """
        Fetch the currently authenticated user using the stored access token.
        """
        response = requests.get(
            f"{BASE_URL}/api/v1/auth/me",
            headers=cls.get_headers(),
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def logout(cls):
        """
        Clear the in-memory session.
        """
        cls.access_token = None
        cls.current_user = None

    @classmethod
    def get_headers(cls):
        """
        Build request headers for authenticated backend calls.
        """
        if not cls.access_token:
            return {}

        return {
            "Authorization": f"Bearer {cls.access_token}"
        }

    @classmethod
    def get_users(cls):
        response = requests.get(
            f"{BASE_URL}/api/v1/users",
            headers=cls.get_headers(),
        )
        return response.json()

    @classmethod
    def add_user(cls, user_data):
        response = requests.post(
            f"{BASE_URL}/api/v1/users",
            json=user_data,
            headers=cls.get_headers(),
        )
        return response.json()

    @classmethod
    def fetch_projects(cls):
        """
        Fetch all projects from the backend.
        """
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/projects",
                headers=cls.get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching projects: {e}")
            return []

    @classmethod
    def list_shots(cls, project_id=None):
        """
        Fetch shots from the backend, optionally filtered by project.
        """
        params = {}
        if project_id is not None:
            params["project_id"] = project_id

        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/shots",
                headers=cls.get_headers(),
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching shots: {e}")
            return []

    @classmethod
    def fetch_assets(cls, project_id=None):
        """
        Fetch assets from the backend, optionally filtered by project.
        """
        params = {}
        if project_id is not None:
            params["project_id"] = project_id

        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/assets",
                headers=cls.get_headers(),
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching assets: {e}")
            return []