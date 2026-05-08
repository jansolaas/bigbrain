from dotenv import load_dotenv
import os
import requests

from pprint import pprint

# Load environment variables from .env
load_dotenv()

# Get the port from the environment variable, with a fallback default
port = os.getenv("PORT", "8000")

# Dynamically build the URL
url = f"http://127.0.0.1:{port}/api/v1/shots"

# Example: Token from login (if required)
access_token = "your_access_token_here"  # Replace with your token from test_login.py

# Set headers if authentication is required
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make GET request to fetch all shots
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print("Response JSON:")
print(response.json())

pprint(response.json())