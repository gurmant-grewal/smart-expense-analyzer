def test_openapi_exists(client):

    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_docs_exist(client):

    response = client.get("/docs")

    assert response.status_code == 200


def test_invalid_endpoint(client):

    response = client.get("/this-endpoint-does-not-exist")

    assert response.status_code == 404