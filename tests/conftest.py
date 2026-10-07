import os
from dotenv import load_dotenv

load_dotenv()


print(f"PYTHONPATH CONFIGTEST: {os.environ.get('PYTHONPATH')}")

def test_create_version(test_client):
    # Create a sample project first
    project_payload = {"name": "TestProject"}
    project_response = test_client.post("/api/v1/projects", json=project_payload)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Create a version for the project
    version_payload = {
        "asset_id": project_id,
        "file_path": "/path/to/version/file",
        "comment": "Initial version through test",
        "version_type": "image_stack",
        "department": "modeling",
        "task": "rigging"
    }

    version_response = test_client.post("/api/v1/versions", json=version_payload)
    assert version_response.status_code == 201
    version_data = version_response.json()

    assert version_data["version_number"] == 1
