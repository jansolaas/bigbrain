# from dotenv import load_dotenv
# import subprocess
#
# # Load environment variables from .env
# load_dotenv()
#
# # Run Uvicorn with the app module specified
# subprocess.run(["uvicorn", "app.main:app", "--reload"])

from dotenv import load_dotenv
import os
import subprocess

# Load environment variables from .env
load_dotenv()

# Get the port from the environment variable, with a fallback default
port = os.getenv("BACKEND_PORT", "8000")

# Run Uvicorn with the app module and dynamic port
subprocess.run(["uvicorn", "app.main:app", "--reload", "--port", port])
