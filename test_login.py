from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

# Get the port from the environment variable, with a fallback default
port = os.getenv("BACKEND_PORT", "8000")

print("port", port)

# Login
login_url = f"http://127.0.0.1:{port}/api/v1/auth/login"
payload = {
    "username": "PythonSaurus",
    "password": "autosaurus"
}

login_response = requests.post(login_url, data=payload)

print("Login status:", login_response.status_code)
print("Login response:")
print(login_response.json())

login_data = login_response.json()
access_token = login_data.get("access_token")

# Test /me
if access_token:
    me_url = f"http://127.0.0.1:{port}/api/v1/auth/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    me_response = requests.get(me_url, headers=headers)

    print("Me status:", me_response.status_code)
    print("Me response:")
    print(me_response.json())