def test_login_success(client):
    res = client.post("/auth/login", json={"username": "admin", "password": "admin"})
    assert res.status_code == 200
    assert "access_token" in res.json
    assert res.json["token_type"] == "bearer"


def test_login_fail(client):
    res = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert res.status_code == 401
