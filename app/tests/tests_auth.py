def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "new@test.com",
        "name": "New User",
        "number": "123456789",
        "password": "Test1234"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "new@test.com"
    assert "password" not in response.json()


def test_register_duplicate_email(client, test_user):
    response = client.post("/auth/register", json={
        "email": "user@test.com",
        "name": "Duplicate",
        "number": "123456789",
        "password": "Test1234"
    })
    assert response.status_code == 409


def test_register_weak_password(client):
    response = client.post("/auth/register", json={
        "email": "weak@test.com",
        "name": "Weak",
        "number": "123456789",
        "password": "123"
    })
    assert response.status_code == 422


def test_register_invalid_email(client):
    response = client.post("/auth/register", json={
        "email": "not-an-email",
        "name": "Invalid",
        "number": "123456789",
        "password": "Test1234"
    })
    assert response.status_code == 422


def test_login_success(client, test_user):
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "Test1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "WrongPass1"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={
        "email": "ghost@test.com",
        "password": "Test1234"
    })
    assert response.status_code == 401