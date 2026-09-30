def test_daily_summary(client, auth_headers):

    response = client.get(
        "/summary/daily",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary_type" in data
    assert "data" in data


def test_weekly_summary(client, auth_headers):

    response = client.get(
        "/summary/weekly",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_monthly_summary(client, auth_headers):

    response = client.get(
        "/summary/monthly",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_invalid_summary(client, auth_headers):

    response = client.get(
        "/summary/yearly",
        headers=auth_headers
    )

    assert response.status_code in [400, 422]


def test_summary_requires_login(client):

    response = client.get(
        "/summary/daily"
    )

    assert response.status_code == 401