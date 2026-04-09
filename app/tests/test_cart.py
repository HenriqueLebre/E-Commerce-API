def test_add_item_to_cart(client, auth_header, test_product):
    response = client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 2
    }, headers=auth_header)
    assert response.status_code == 200


def test_add_item_unauthorized(client, test_product):
    response = client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 1
    })
    assert response.status_code == 401


def test_add_item_exceeds_stock(client, auth_header, test_product):
    response = client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 9999
    }, headers=auth_header)
    assert response.status_code == 400


def test_add_invalid_product(client, auth_header):
    response = client.post("/cart/items", json={
        "product_id": 9999,
        "quantity": 1
    }, headers=auth_header)
    assert response.status_code == 404


def test_get_cart(client, auth_header, test_product):
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 1
    }, headers=auth_header)

    response = client.get("/cart", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


def test_remove_item_from_cart(client, auth_header, test_product):
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 1
    }, headers=auth_header)

    cart = client.get("/cart", headers=auth_header).json()
    item_id = cart["items"][0]["id"]

    response = client.delete(f"/cart/items/{item_id}", headers=auth_header)
    assert response.status_code == 200