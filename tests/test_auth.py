def test_admin_login(client, admin_login_user):
    response = client.post(
        "/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "testpassword"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [401, 403]


def test_login_invalid_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code in [401, 404]


def test_login_missing_email(client):
    response = client.post(
        "/auth/login",
        json={
            "password": "testpassword"
        }
    )

    assert response.status_code == 422


def test_login_missing_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "testadmin@example.com"
        }
    )

    assert response.status_code == 422
    
    
    
def test_sales_executive_login(client, db):
    from src.models.user import UserModel
    from src.utils.security import hash_password

    user = UserModel(
        full_name="Test Sales",
        email="salestest@example.com",
        password=hash_password("testpassword"),
        role="Sales Executive"
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "salestest@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_inventory_manager_login(client, db):
    from src.models.user import UserModel
    from src.utils.security import hash_password

    user = UserModel(
        full_name="Test Inventory Manager",
        email="inventorytest@example.com",
        password=hash_password("testpassword"),
        role="Inventory Manager"
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "inventorytest@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, admin_login_user):
    response = client.post(
        "/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "completelywrong"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password"


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "userdoesnotexist@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password"


def test_login_returns_bearer_token(client, admin_login_user):
    response = client.post(
        "/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20
    assert data["token_type"] == "bearer"
    
    
    
def test_sales_executive_cannot_create_product(
    client,
    sales_executive_token
):
    headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    response = client.post(
        "/product/create",
        json={
            "name": "Unauthorized Product",
            "description": "Should not be created",
            "sku": "UNAUTHORIZED-001",
            "price": 500,
            "quantity": 10,
            "category_id": 1
        },
        headers=headers
    )

    assert response.status_code == 403


def test_inventory_manager_cannot_create_product(
    client,
    inventory_manager_token
):
    headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    response = client.post(
        "/product/create",
        json={
            "name": "Unauthorized Product",
            "description": "Should not be created",
            "sku": "UNAUTHORIZED-002",
            "price": 500,
            "quantity": 10,
            "category_id": 1
        },
        headers=headers
    )

    assert response.status_code == 403


def test_admin_cannot_create_sale(
    client,
    admin_token
):
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.post(
        "/sales/",
        json={
            "invoice_number": "AUTH-TEST-001",
            "customer_name": "Authorization Test",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1,
                    "unit_price": 500
                }
            ]
        },
        headers=headers
    )

    assert response.status_code == 403


def test_sales_executive_cannot_create_purchase(
    client,
    sales_executive_token
):
    headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    response = client.post(
        "/purchase/",
        json={
            "supplier_id": 999999,
            "invoice_number": "AUTH-PURCHASE-001",
            "purchase_date": "2026-08-12",
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1,
                    "unit_price": 500
                }
            ]
        },
        headers=headers
    )

    assert response.status_code == 403


def test_inventory_manager_cannot_create_sale(
    client,
    inventory_manager_token
):
    headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    response = client.post(
        "/sales/",
        json={
            "invoice_number": "AUTH-SALE-001",
            "customer_name": "Authorization Test",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1,
                    "unit_price": 500
                }
            ]
        },
        headers=headers
    )

    assert response.status_code == 403