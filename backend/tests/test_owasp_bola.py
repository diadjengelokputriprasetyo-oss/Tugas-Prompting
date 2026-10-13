def test_owasp_bola_access_control(client):
    # 1. Register and login User A
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "User Alpha",
            "email": "alpha@autopartsmart.com",
            "password": "PasswordAlpha123!",
        },
    )
    resp_a = client.post(
        "/api/v1/auth/login",
        json={"email": "alpha@autopartsmart.com", "password": "PasswordAlpha123!"},
    )
    token_a = resp_a.json()["access_token"]

    # 2. User A creates a confidential prediction
    pred_resp = client.post(
        "/api/v1/predictions",
        json={
            "input_data": {
                "item_id": "PART-ALPHA-CONFIDENTIAL",
                "lag_1": 25,
                "lag_2": 20,
                "lag_3": 18,
            }
        },
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert pred_resp.status_code == 201
    pred_id = pred_resp.json()["id"]

    # 3. Register and login User B (Attacker / Unauthorized user)
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "User Beta (Attacker)",
            "email": "beta@autopartsmart.com",
            "password": "PasswordBeta123!",
        },
    )
    resp_b = client.post(
        "/api/v1/auth/login",
        json={"email": "beta@autopartsmart.com", "password": "PasswordBeta123!"},
    )
    token_b = resp_b.json()["access_token"]

    # 4. User B attempts BOLA exploit by directly accessing User A's prediction ID
    attack_resp = client.get(
        f"/api/v1/predictions/{pred_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    # OWASP API1:2023 Anti-BOLA: MUST be rejected with HTTP 403 Forbidden
    assert attack_resp.status_code == 403
    assert "BOLA Protection" in attack_resp.json()["message"]

    # 5. User B lists predictions -> should be empty, isolated from User A's records
    list_b_resp = client.get(
        "/api/v1/predictions",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert list_b_resp.status_code == 200
    assert len(list_b_resp.json()) == 0

    # 6. User A accesses own prediction -> HTTP 200 OK
    legit_resp = client.get(
        f"/api/v1/predictions/{pred_id}",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert legit_resp.status_code == 200
    assert legit_resp.json()["id"] == pred_id
