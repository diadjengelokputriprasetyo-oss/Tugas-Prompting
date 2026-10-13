def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Budi Santoso",
            "email": "budi@autopartsmart.com",
            "password": "PasswordSuper123!",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "budi@autopartsmart.com"
    assert data["full_name"] == "Budi Santoso"
    assert "id" in data
    assert "password_hash" not in data  # Never expose password hash!


def test_register_duplicate_email(client):
    payload = {
        "full_name": "Budi Santoso",
        "email": "duplicate@autopartsmart.com",
        "password": "PasswordSuper123!",
    }
    r1 = client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 400
    assert "Email sudah terdaftar" in r2.json()["message"]


def test_login_success_and_token_pair(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Pak Budi",
            "email": "budi_login@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )

    # Login
    login_resp = client.post(
        "/api/v1/auth/login",
        json={
            "email": "budi_login@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Pak Budi",
            "email": "budi_fail@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )

    login_resp = client.post(
        "/api/v1/auth/login",
        json={
            "email": "budi_fail@autopartsmart.com",
            "password": "WrongPassword!",
        },
    )
    assert login_resp.status_code == 401


def test_protected_me_endpoint(client):
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Pak Budi",
            "email": "me_test@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={
            "email": "me_test@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )
    access_token = login_resp.json()["access_token"]

    # Without token -> 401
    unauth_resp = client.get("/api/v1/auth/me")
    assert unauth_resp.status_code == 401

    # With Bearer token -> 200
    auth_resp = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert auth_resp.status_code == 200
    assert auth_resp.json()["email"] == "me_test@autopartsmart.com"


def test_refresh_token_endpoint(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Pak Budi",
            "email": "refresh_test@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh_test@autopartsmart.com",
            "password": "ValidPassword123!",
        },
    )
    refresh_token = login_resp.json()["refresh_token"]

    ref_resp = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert ref_resp.status_code == 200
    new_data = ref_resp.json()
    assert "access_token" in new_data
