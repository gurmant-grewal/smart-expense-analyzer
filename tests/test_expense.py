
def test_analyze_expense(client):

    response = client.post(
        "/expenses/analyze",
        json={
            "text": "Pizza from Dominos",
            "amount": 550,
            "date": "2026-07-15",
            "predicted_category": "",
            "corrected_category": None
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "category" in data
    assert "confidence" in data
    assert "merchant" in data

def test_empty_text(client):

    response = client.post(

        "/expenses/analyze",

        json={

            "text": "",

            "amount": 500,

            "date": "2026-07-15",

            "predicted_category": "",

            "corrected_category": None

        }

    )

    assert response.status_code == 422

def test_invalid_amount(client):

    response = client.post(
        "/expenses/analyze",
        json={
            "text": "Pizza",
            "amount": -50,
            "date": "2026-07-15",
            "predicted_category": "",
            "corrected_category": None
        }
    )

    assert response.status_code == 422

def test_add_expense(client, auth_headers):

    response = client.post(
        "/expenses",
        headers=auth_headers,
        json={
            "text": "Netflix Subscription",
            "amount": 699,
            "date": "2026-07-15",
            "predicted_category": "entertainment",
            "corrected_category": None
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Expense added."
    assert "expense_id" in data

def test_add_expense_without_token(client):

    response = client.post(
        "/expenses",
        json={
            "text": "Netflix",
            "amount": 699,
            "date": "2026-07-15",
            "predicted_category": "entertainment",
            "corrected_category": None
        }
    )

    assert response.status_code == 401

def test_invalid_token(client):

    response = client.post(
        "/expenses",
        headers={
            "Authorization": "Bearer invalidtoken"
        },
        json={
            "text": "Netflix",
            "amount": 699,
            "date": "2026-07-15",
            "predicted_category": "entertainment",
            "corrected_category": None
        }
    )

    assert response.status_code in [401, 403]

def test_corrected_category_saved(client, auth_headers):

    response = client.post(
        "/expenses",
        headers=auth_headers,
        json={
            "text": "Pizza",
            "amount": 400,
            "date": "2026-07-15",
            "predicted_category": "shopping",
            "corrected_category": "food"
        }
    )

    assert response.status_code == 200

def test_large_amount(client):

    response = client.post(
        "/expenses/analyze",
        json={
            "text": "Laptop",
            "amount": 100000000,
            "date": "2026-07-15",
            "predicted_category": "",
            "corrected_category": None
        }
    )

    assert response.status_code == 422

