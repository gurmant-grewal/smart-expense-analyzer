from app.security.password_security import (
    hash_password,
    verify_password,
)
from app.security.auth import (
    create_access_token,
    verify_token,
)


def test_hash_password_changes_value():

    password = "mypassword"

    hashed = hash_password(password)

    assert hashed != password


def test_hash_is_string():

    hashed = hash_password("mypassword")

    assert isinstance(hashed, str)


def test_verify_correct_password():

    password = "mypassword"

    hashed = hash_password(password)

    assert verify_password(password, hashed)


def test_verify_wrong_password():

    password = "mypassword"

    hashed = hash_password(password)

    assert not verify_password(
        "wrongpassword",
        hashed
    )


def test_same_password_generates_different_hashes():

    password = "mypassword"

    hash1 = hash_password(password)

    hash2 = hash_password(password)

    assert hash1 != hash2


def test_create_access_token():

    token = create_access_token(
        {"sub": "testuser"}
    )

    assert isinstance(token, str)

    assert len(token) > 20


def test_verify_token():

    token = create_access_token(
        {"sub": "testuser"}
    )

    payload = verify_token(token)

    assert payload["sub"] == "testuser"

def test_login_success(client):

    client.post(
    "/register",
    json={
            "username": "testuser",
            "password": "password123"
        }
)
    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"

def test_duplicate_registration(client):

    client.post(
        "/register",
        json={
            "username": "duplicate",
            "password": "password123"
        }
    )

    response = client.post(
        "/register",
        json={
            "username": "duplicate",
            "password": "password123"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "username already exists" 
    
def test_login_wrong_password(client):

    client.post(
        "/register",
        json={
            "username": "john",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "john",
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [400, 401]

def test_login_unknown_user(client):

    response = client.post(
        "/login",
        json={
            "username": "unknown",
            "password": "password123"
        }
    )

    assert response.status_code in [400, 404]

