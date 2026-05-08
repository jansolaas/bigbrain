from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

# Get the port from the environment variable, with a fallback default
port = os.getenv("PORT", "8000")

# Dynamically build the URL
url = f"http://127.0.0.1:{port}/api/v1/auth/login"
payload = {
    "username": "PythonSaurus",
    "password": "autosaurus"
}
response = requests.post(url, data=payload)

print(response.status_code)
print(response.json())
