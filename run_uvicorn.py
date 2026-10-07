from dotenv import load_dotenv
import os
import subprocess

# Load environment variables
load_dotenv()

# Fetch port and host
port = os.getenv("BACKEND_PORT", "8000")
host = os.getenv("BACKEND_HOST", "127.0.0.1")
use_reload = os.getenv("UVICORN_RELOAD", "true") == "true"
workers = os.getenv("UVICORN_WORKERS", "1")

# Command setup
command = [
    "uvicorn",
    "app.main:app",
    "--host", host,
    "--port", port,
    "--workers", workers,
]

# Add the reload flag in development
if use_reload:
    command.append("--reload")

subprocess.run(command)
