def _token(client, username="admin", password="admin"):
    res = client.post("/auth/login", json={"username": username, "password": password})
    return res.json()["access_token"]


def test_books_requires_auth(client):
    res = client.get("/books")
    assert res.status_code == 401


def test_reader_cannot_write(client):
    token = _token(client, "reader", "reader")
    res = client.post(
        "/books",
        json={"title": "X", "author": "Y", "date_publish": "2020-01-01"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403  # falta books:write


def test_crud_books_admin(client):
    token = _token(client, "admin", "admin")
    headers = {"Authorization": f"Bearer {token}"}

    # create
    r1 = client.post(
        "/books",
        json={"title": "Clean Code", "author": "Robert Martin", "date_publish": "2008-01-01"},
        headers=headers,
    )
    assert r1.status_code == 201
    book_id = r1.json()["id"]

    # list
    r2 = client.get("/books", headers=headers)
    assert r2.status_code == 200
    assert len(r2.json()["items"]) == 1

    # get
    r3 = client.get(f"/books/{book_id}", headers=headers)
    assert r3.status_code == 200
    assert r3.json()["title"] == "Clean Code"

    # patch
    r4 = client.patch(f"/books/{book_id}", json={"date_publish": "2009-01-01"}, headers=headers)
    assert r4.status_code == 200
    assert r4.json()["date_publish"] == "2009-01-01"

    # delete
    r5 = client.delete(f"/books/{book_id}", headers=headers)
    assert r5.status_code == 204
