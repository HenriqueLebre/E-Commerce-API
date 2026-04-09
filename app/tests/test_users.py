def test_get_my_profile(client, auth_header, test_user):
    response = client.get("/users/me", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"


def test_get_my_profile_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_update_my_profile(client, auth_header, test_user):
    response = client.put("/users/me", json={
        "name": "Updated Name"
    }, headers=auth_header)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_list_users_as_admin(client, admin_header, test_user):
    response = client.get("/users/", headers=admin_header)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_list_users_as_user_forbidden(client, auth_header):
    response = client.get("/users/", headers=auth_header)
    assert response.status_code == 403


def test_get_user_by_id_as_admin(client, admin_header, test_user):
    response = client.get(f"/users/{test_user.id}", headers=admin_header)
    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"


def test_deactivate_user_as_admin(client, admin_header, test_user):
    response = client.delete(f"/users/{test_user.id}", headers=admin_header)
    assert response.status_code == 200
    assert response.json()["active"] is False


def test_deactivate_user_as_user_forbidden(client, auth_header, test_user):
    response = client.delete(f"/users/{test_user.id}", headers=auth_header)
    assert response.status_code == 403