from datetime import date


def test_create_purchase(client, admin_token, inventory_manager_token):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # -------------------------
    # Create category as Admin
    # -------------------------
    category_payload = {
        "name": "Purchase Test Category",
        "description": "Category for purchase testing"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # -------------------------
    # Create product as Admin
    # -------------------------
    product_payload = {
        "name": "Purchase Test Product",
        "description": "Product for purchase testing",
        "sku": "PURCHASE-TEST-001",
        "price": 500,
        "quantity": 10,
        "category_id": category_id
    }

    product_response = client.post(
        "/product/create",
        json=product_payload,
        headers=admin_headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # -------------------------
    # Create supplier as Admin
    # -------------------------
    supplier_payload = {
        "name": "Purchase Test Supplier",
        "company_name": "Purchase Supplies Pvt Ltd",
        "email": "purchase@test.com",
        "phone": "9876543221",
        "address": "Ludhiana, Punjab"
    }

    supplier_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=admin_headers
    )

    assert supplier_response.status_code == 201

    supplier_id = supplier_response.json()["id"]

    # -------------------------
    # Create purchase as Inventory Manager
    # -------------------------
    purchase_payload = {
        "supplier_id": supplier_id,
        "invoice_number": "INV-TEST-001",
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": product_id,
                "quantity": 5,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/purchase/",
        json=purchase_payload,
        headers=inventory_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 201

    data = response.json()

    # -------------------------
    # Verify purchase
    # -------------------------
    assert data["supplier_id"] == supplier_id
    assert data["invoice_number"] == "INV-TEST-001"
    assert data["purchase_date"] == str(date.today())
    assert data["status"] == "Completed"

    # 1 purchase item
    assert len(data["items"]) == 1

    # Verify item
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 5
    assert data["items"][0]["unit_price"] == 500

    # Verify subtotal
    assert data["items"][0]["subtotal"] == 2500

    # Verify total
    assert data["total_amount"] == 2500
    
    
    
def test_get_all_purchases(client, admin_token, inventory_manager_token):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Get Purchase Category",
            "description": "Testing purchase retrieval"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Get Purchase Product",
            "description": "Testing purchase retrieval",
            "sku": "GET-PURCHASE-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Get Purchase Supplier",
            "company_name": "Get Purchase Company",
            "email": "getpurchase@test.com",
            "phone": "9876543231",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201
    supplier_id = supplier_response.json()["id"]

    # Create purchase
    purchase_response = client.post(
        "/purchase/",
        json={
            "supplier_id": supplier_id,
            "invoice_number": "GET-INV-001",
            "purchase_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5,
                    "unit_price": 500
                }
            ]
        },
        headers=inventory_headers
    )

    assert purchase_response.status_code == 201

    # Get all purchases
    response = client.get(
        "/purchase/all_purchase",
        headers=inventory_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    
def test_get_purchase_by_id(client, admin_token, inventory_manager_token):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Get By ID Category",
            "description": "Testing purchase by ID"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Get By ID Product",
            "description": "Testing purchase by ID",
            "sku": "GET-BY-ID-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Get By ID Supplier",
            "company_name": "Get By ID Company",
            "email": "getbyid@test.com",
            "phone": "9876543241",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201
    supplier_id = supplier_response.json()["id"]

    # Create purchase
    purchase_response = client.post(
        "/purchase/",
        json={
            "supplier_id": supplier_id,
            "invoice_number": "BY-ID-INV-001",
            "purchase_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5,
                    "unit_price": 500
                }
            ]
        },
        headers=inventory_headers
    )

    assert purchase_response.status_code == 201

    purchase_id = purchase_response.json()["id"]

    # Get purchase by ID
    response = client.get(
        f"/purchase/purchase/{purchase_id}",
        headers=inventory_headers
    )

    assert response.status_code == 200

    data = response.json()

    # Verify purchase
    assert data["id"] == purchase_id
    assert data["supplier_id"] == supplier_id
    assert data["invoice_number"] == "BY-ID-INV-001"

    # Verify item
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 5
    
    
def test_update_purchase(client, admin_token, inventory_manager_token):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Update Purchase Category",
            "description": "Testing purchase update"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Update Purchase Product",
            "description": "Testing purchase update",
            "sku": "UPDATE-PURCHASE-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Update Purchase Supplier",
            "company_name": "Update Purchase Company",
            "email": "updatepurchase@test.com",
            "phone": "9876543251",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201
    supplier_id = supplier_response.json()["id"]

    # Create purchase
    purchase_response = client.post(
        "/purchase/",
        json={
            "supplier_id": supplier_id,
            "invoice_number": "UPDATE-INV-001",
            "purchase_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5,
                    "unit_price": 500
                }
            ]
        },
        headers=inventory_headers
    )

    assert purchase_response.status_code == 201

    purchase_id = purchase_response.json()["id"]

    # Update purchase
    update_payload = {
        "supplier_id": supplier_id,
        "invoice_number": "UPDATE-INV-002",
        "purchase_date": "2026-08-13",
        "items": [
            {
                "product_id": product_id,
                "quantity": 10,
                "unit_price": 600
            }
        ]
    }

    response = client.put(
        f"/purchase/update/{purchase_id}",
        json=update_payload,
        headers=inventory_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200

    data = response.json()

    # Verify updated purchase
    assert data["id"] == purchase_id
    assert data["supplier_id"] == supplier_id
    assert data["invoice_number"] == "UPDATE-INV-002"
    assert data["purchase_date"] == "2026-08-13"

    # Verify updated item
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 10
    assert data["items"][0]["unit_price"] == 600

    # Verify total
    assert data["total_amount"] == 6000
    
    
def test_delete_purchase(client, admin_token, inventory_manager_token):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Delete Purchase Category",
            "description": "Testing purchase deletion"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Delete Purchase Product",
            "description": "Testing purchase deletion",
            "sku": "DELETE-PURCHASE-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Delete Purchase Supplier",
            "company_name": "Delete Purchase Company",
            "email": "deletepurchase@test.com",
            "phone": "9876543261",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201
    supplier_id = supplier_response.json()["id"]

    # Create purchase
    purchase_response = client.post(
        "/purchase/",
        json={
            "supplier_id": supplier_id,
            "invoice_number": "DELETE-INV-001",
            "purchase_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5,
                    "unit_price": 500
                }
            ]
        },
        headers=inventory_headers
    )

    assert purchase_response.status_code == 201

    purchase_id = purchase_response.json()["id"]

    # Delete purchase as Admin
    response = client.delete(
        f"/purchase/delete/{purchase_id}",
        headers=admin_headers
    )

    assert response.status_code == 204

    # Verify purchase no longer exists
    get_response = client.get(
        f"/purchase/purchase/{purchase_id}",
        headers=inventory_headers
    )

    assert get_response.status_code == 404
    
    
def test_create_purchase_invalid_supplier(
    client,
    inventory_manager_token
):

    headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    purchase_payload = {
        "supplier_id": 999999,
        "invoice_number": "INVALID-SUPPLIER-001",
        "purchase_date": "2026-08-12",
        "items": [
            {
                "product_id": 1,
                "quantity": 5,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/purchase/",
        json=purchase_payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 404
    
    
def test_create_purchase_invalid_product(
    client,
    admin_token,
    inventory_manager_token
):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Invalid Product Supplier",
            "company_name": "Invalid Product Company",
            "email": "invalidproduct@test.com",
            "phone": "9876543271",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201

    supplier_id = supplier_response.json()["id"]

    # Use a product ID that does not exist
    purchase_payload = {
        "supplier_id": supplier_id,
        "invoice_number": "INVALID-PRODUCT-001",
        "purchase_date": "2026-08-12",
        "items": [
            {
                "product_id": 999999,
                "quantity": 5,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/purchase/",
        json=purchase_payload,
        headers=inventory_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 404
    
    
def test_create_purchase_invalid_quantity(
    client,
    admin_token,
    inventory_manager_token
):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Invalid Quantity Supplier",
            "company_name": "Invalid Quantity Company",
            "email": "invalidquantity@test.com",
            "phone": "9876543281",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201

    supplier_id = supplier_response.json()["id"]

    # Invalid quantity = 0
    purchase_payload = {
        "supplier_id": supplier_id,
        "invoice_number": "INVALID-QTY-001",
        "purchase_date": "2026-08-12",
        "items": [
            {
                "product_id": 1,
                "quantity": 0,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/purchase/",
        json=purchase_payload,
        headers=inventory_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 422
    
    
def test_create_purchase_invalid_unit_price(
    client,
    admin_token,
    inventory_manager_token
):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # Create supplier
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Invalid Price Supplier",
            "company_name": "Invalid Price Company",
            "email": "invalidprice@test.com",
            "phone": "9876543291",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201

    supplier_id = supplier_response.json()["id"]

    # Invalid unit price = 0
    purchase_payload = {
        "supplier_id": supplier_id,
        "invoice_number": "INVALID-PRICE-001",
        "purchase_date": "2026-08-12",
        "items": [
            {
                "product_id": 1,
                "quantity": 5,
                "unit_price": 0
            }
        ]
    }

    response = client.post(
        "/purchase/",
        json=purchase_payload,
        headers=inventory_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 422
    
    
def test_purchase_increases_stock(
    client,
    admin_token,
    inventory_manager_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    inventory_headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    # -------------------------
    # Create category as Admin
    # -------------------------
    category_response = client.post(
        "/category/create",
        json={
            "name": "Stock Purchase Category",
            "description": "Testing stock increase"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # -------------------------
    # Create product as Admin
    # Initial stock = 10
    # -------------------------
    product_response = client.post(
        "/product/create",
        json={
            "name": "Stock Purchase Product",
            "description": "Testing stock increase",
            "sku": "STOCK-PURCHASE-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # Verify initial stock
    assert product_response.json()["quantity"] == 10

    # -------------------------
    # Create supplier as Admin
    # -------------------------
    supplier_response = client.post(
        "/supplier/create",
        json={
            "name": "Stock Purchase Supplier",
            "company_name": "Stock Purchase Company",
            "email": "stockpurchase@test.com",
            "phone": "9876543301",
            "address": "Ludhiana, Punjab"
        },
        headers=admin_headers
    )

    assert supplier_response.status_code == 201

    supplier_id = supplier_response.json()["id"]

    # -------------------------
    # Create purchase as
    # Inventory Manager
    # -------------------------
    purchase_response = client.post(
        "/purchase/",
        json={
            "supplier_id": supplier_id,
            "invoice_number": "STOCK-INV-001",
            "purchase_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5,
                    "unit_price": 500
                }
            ]
        },
        headers=inventory_headers
    )

    assert purchase_response.status_code == 201

    purchase_data = purchase_response.json()

    # Verify purchase was created
    assert purchase_data["supplier_id"] == supplier_id
    assert len(purchase_data["items"]) == 1
    assert purchase_data["items"][0]["product_id"] == product_id
    assert purchase_data["items"][0]["quantity"] == 5
    assert purchase_data["items"][0]["unit_price"] == 500

    # -------------------------
    # Get product after purchase
    # -------------------------
    product_response = client.get(
        f"/product/product/{product_id}",
        headers=inventory_headers
    )

    assert product_response.status_code == 200

    product_data = product_response.json()

    # -------------------------
    # Verify stock increased
    # 10 + 5 = 15
    # -------------------------
    assert product_data["id"] == product_id
    assert product_data["quantity"] == 15