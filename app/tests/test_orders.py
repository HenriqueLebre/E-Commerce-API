def test_checkout_success(client, auth_header, test_product, db):
    # Adiciona item ao carrinho
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 2
    }, headers=auth_header)

    response = client.post("/orders/checkout", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["order"]["status"] == "pending"
    assert "payment_url" in response.json()


def test_checkout_empty_cart(client, auth_header):
    response = client.post("/orders/checkout", headers=auth_header)
    assert response.status_code == 400


def test_list_orders(client, auth_header, test_product):
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 1
    }, headers=auth_header)
    client.post("/orders/checkout", headers=auth_header)

    response = client.get("/orders/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_order_by_id(client, auth_header, test_product):
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 1
    }, headers=auth_header)
    checkout = client.post("/orders/checkout", headers=auth_header).json()
    order_id = checkout["order"]["id"]

    response = client.get(f"/orders/{order_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_get_order_not_found(client, auth_header):
    response = client.get("/orders/9999", headers=auth_header)
    assert response.status_code == 404


def test_list_all_orders_as_admin(client, admin_header):
    response = client.get("/orders/admin/all", headers=admin_header)
    assert response.status_code == 200


def test_list_all_orders_as_user_forbidden(client, auth_header):
    response = client.get("/orders/admin/all", headers=auth_header)
    assert response.status_code == 403


def test_checkout_decrements_stock(client, auth_header, test_product, db):
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 5
    }, headers=auth_header)
    client.post("/orders/checkout", headers=auth_header)

    response = client.get(f"/products/{test_product.id}")
    assert response.json()["stock"] == 95


def test_checkout_clears_cart(client, auth_header, test_product):
    client.post("/cart/items", json={
        "product_id": test_product.id,
        "quantity": 1
    }, headers=auth_header)
    client.post("/orders/checkout", headers=auth_header)

    cart = client.get("/cart", headers=auth_header).json()
    assert len(cart["items"]) == 0