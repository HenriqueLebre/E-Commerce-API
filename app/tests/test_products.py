def test_list_products_public(client, test_product):
    response = client.get("/products/")
    assert response.status_code == 200


def test_get_product_by_id(client, test_product):
    response = client.get(f"/products/{test_product.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


def test_get_product_not_found(client):
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_create_product_as_admin(client, admin_header):
    response = client.post("/products/", json={
        "name": "New Product",
        "description": "Description",
        "price": 29.90,
        "stock": 50,
        "category": "test"
    }, headers=admin_header)
    assert response.status_code == 200
    assert response.json()["name"] == "New Product"


def test_create_product_as_user_forbidden(client, auth_header):
    response = client.post("/products/", json={
        "name": "Forbidden Product",
        "description": "Description",
        "price": 29.90,
        "stock": 50,
        "category": "test"
    }, headers=auth_header)
    assert response.status_code == 403


def test_create_product_unauthorized(client):
    response = client.post("/products/", json={
        "name": "No Auth Product",
        "description": "Description",
        "price": 29.90,
        "stock": 50,
        "category": "test"
    })
    assert response.status_code == 401


def test_update_product_as_admin(client, admin_header, test_product):
    response = client.put(f"/products/{test_product.id}", json={
        "name": "Updated Product"
    }, headers=admin_header)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"


def test_delete_product_as_admin(client, admin_header, test_product):
    response = client.delete(f"/products/{test_product.id}", headers=admin_header)
    assert response.status_code == 200


def test_delete_product_as_user_forbidden(client, auth_header, test_product):
    response = client.delete(f"/products/{test_product.id}", headers=auth_header)
    assert response.status_code == 403