def test_get_projects(test_client):
    url = "/api/v1/projects"
    headers = {
        "Authorization": "Bearer dummy_access_token"
    }

    response = test_client.get(url, headers=headers)
    assert response.status_code == 200
    response_data = response.json()

    assert isinstance(response_data, list)
    if response_data:
        assert "id" in response_data[0]
        assert "name" in response_data[0]
