from dotenv import load_dotenv
import subprocess

# Load environment variables from .env
load_dotenv()

# Run Uvicorn with the app module specified
subprocess.run(["uvicorn", "app.main:app", "--reload"])
