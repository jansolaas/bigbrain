from dotenv import load_dotenv
import os
import requests
from typing import AnyStr
from pprint import pprint
import argparse

# Load environment variables from .env
load_dotenv()

def get(somenthing: AnyStr):
    # Get the port from the environment variable, with a fallback default
    port = os.getenv("BACKEND_PORT", "8000")

    # Dynamically build the URL
    url = f"http://127.0.0.1:{port}/api/v1/{somenthing}"

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

    pprint(response.json(), indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retreives desired data from the API.")
    parser.add_argument(
        "--input", "-i", type=str, default=None,
        help="'assets'"
    )
    args = parser.parse_args()
    if args.input:
        inp = args.input
    else:
        print("Ingen input oppgitt – bruker eksempelinput.")
        inp = "shots"
    get(inp)
