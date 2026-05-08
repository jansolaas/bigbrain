import requests
AUTH_TOKEN = "your_jwt_token_here"  # Replace with the user's JWT token
BASE_URL = "http://127.0.0.1:8000"  # Replace with your FastAPI URL


class BackendService:

    @staticmethod
    def get_users():
        response = requests.get(f"{BackendService.BASE_URL}/users")
        return response.json()

    @staticmethod
    def add_user(user_data):
        response = requests.post(f"{BackendService.BASE_URL}/users", json=user_data)
        return response.json()

    def fetch_assets(self):
        """
        Fetch hierarchical assets from the backend.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        try:
            response = requests.get(f"{BASE_URL}/api/v1/assets/", headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad HTTP responses.
            data = response.json()
            return data  # Assuming the backend returns JSON data in the same format.
        except requests.RequestException as e:
            print(f"Error fetching assets: {e}")
            return []  # Return an empty list on failure.
