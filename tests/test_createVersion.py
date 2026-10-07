import os

print(f"PYTHONPATH CREATEVERSION: {os.environ.get('PYTHONPATH')}")
# import backend.app

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app  # Import your FastAPI app
from backend.app.database import SessionLocal
from backend.app.models import Asset, Version

client = TestClient(app)

# Use a test database (e.g., SQLite in-memory or a test-specific SQLite file)
@pytest.fixture(autouse=True)
def setup_and_teardown():
    db = SessionLocal()
    yield db
    db.close()


def test_create_version():
    # Create a test asset
    asset_payload = {
        "name": "TestAsset",
        "project_id": 1,  # Assuming seeded project ID
        "shot_id": 1  # Assuming seeded shot ID
    }
    asset_response = client.post("/assets", json=asset_payload)
    assert asset_response.status_code == 201
    asset_id = asset_response.json()["id"]

    # Create a version for the asset
    version_payload = {
        "asset_id": asset_id,
        "file_path": "/path/to/version/file",
        "comment": "Initial version through test",
        "version_type": "image_stack",
        "department": "modeling",
        "task": "rigging"
    }
    version_response = client.post("/versions", json=version_payload)
    assert version_response.status_code == 201
    version_data = version_response.json()

    # Verify the version number
    assert version_data["version_number"] == 1
    assert version_data["asset_id"] == asset_id
