def test_create_sale(
    client,
    admin_token,
    sales_executive_token
):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # -------------------------
    # Create category as Admin
    # -------------------------
    category_response = client.post(
        "/category/create",
        json={
            "name": "Sales Test Category",
            "description": "Category for sales testing"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # -------------------------
    # Create product as Admin
    # Initial stock = 20
    # -------------------------
    product_response = client.post(
        "/product/create",
        json={
            "name": "Sales Test Product",
            "description": "Product for sales testing",
            "sku": "SALES-TEST-001",
            "price": 500,
            "quantity": 20,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # -------------------------
    # Create sale as Sales Executive
    # -------------------------
    sale_payload = {
        "invoice_number": "SALE-INV-001",
        "customer_name": "Test Customer",
        "sale_date": "2026-08-12",
        "items": [
            {
                "product_id": product_id,
                "quantity": 5,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/sales/",
        json=sale_payload,
        headers=sales_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 201

    data = response.json()

    # -------------------------
    # Verify sale response
    # -------------------------
    assert data["invoice_number"] == "SALE-INV-001"
    assert data["customer_name"] == "Test Customer"
    assert data["status"] == "Completed"

    assert len(data["items"]) == 1

    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 5
    assert data["items"][0]["unit_price"] == 500

    # 5 × 500
    assert data["items"][0]["subtotal"] == 2500

    assert data["total_amount"] == 2500
    
    
def test_get_all_sales(
    client,
    admin_token,
    sales_executive_token
):

    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # -------------------------
    # Create category
    # -------------------------
    category_response = client.post(
        "/category/create",
        json={
            "name": "Get Sales Category",
            "description": "Testing get all sales"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # -------------------------
    # Create product
    # -------------------------
    product_response = client.post(
        "/product/create",
        json={
            "name": "Get Sales Product",
            "description": "Testing get all sales",
            "sku": "GET-SALES-001",
            "price": 400,
            "quantity": 20,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # -------------------------
    # Create sale
    # -------------------------
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "GET-SALES-INV-001",
            "customer_name": "Get Sales Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": 400
                }
            ]
        },
        headers=sales_headers
    )

    assert sale_response.status_code == 201

    # -------------------------
    # Get all sales
    # -------------------------
    response = client.get(
        "/sales/all_sales",
        headers=sales_headers
    )

    assert response.status_code == 200

    data = response.json()

    # Verify response is a list
    assert isinstance(data, list)

    # At least the sale we just created should exist
    assert len(data) >= 1

    # Find our sale
    sale = next(
        sale for sale in data
        if sale["invoice_number"] == "GET-SALES-INV-001"
    )

    assert sale["customer_name"] == "Get Sales Customer"
    assert len(sale["items"]) == 1
    assert sale["items"][0]["product_id"] == product_id
    
    
    
def test_get_sale_by_id(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Sale ID Category",
            "description": "Testing sale by ID"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Sale ID Product",
            "description": "Testing sale by ID",
            "sku": "SALE-ID-001",
            "price": 600,
            "quantity": 20,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Create sale
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "SALE-ID-INV-001",
            "customer_name": "Sale ID Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                    "unit_price": 600
                }
            ]
        },
        headers=sales_headers
    )

    assert sale_response.status_code == 201

    sale_id = sale_response.json()["id"]

    # Get sale by ID
    response = client.get(
        f"/sales/sales/{sale_id}",
        headers=sales_headers
    )

    assert response.status_code == 200

    data = response.json()

    # Verify sale
    assert data["id"] == sale_id
    assert data["invoice_number"] == "SALE-ID-INV-001"
    assert data["customer_name"] == "Sale ID Customer"

    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 3
    assert data["items"][0]["unit_price"] == 600

    assert data["total_amount"] == 1800
    
    
    
def test_update_sale(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # -------------------------
    # Create category
    # -------------------------
    category_response = client.post(
        "/category/create",
        json={
            "name": "Update Sale Category",
            "description": "Testing update sale"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # -------------------------
    # Create product
    # -------------------------
    product_response = client.post(
        "/product/create",
        json={
            "name": "Update Sale Product",
            "description": "Testing update sale",
            "sku": "UPDATE-SALE-001",
            "price": 500,
            "quantity": 30,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # -------------------------
    # Create sale
    # -------------------------
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "UPDATE-SALE-001",
            "customer_name": "Old Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    assert sale_response.status_code == 201

    sale_id = sale_response.json()["id"]

    # -------------------------
    # Update sale
    # -------------------------
    update_response = client.put(
        f"/sales/update/{sale_id}",
        json={
            "invoice_number": "UPDATE-SALE-002",
            "customer_name": "Updated Customer",
            "sale_date": "2026-08-13",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                    "unit_price": 600
                }
            ]
        },
        headers=sales_headers
    )

    print("UPDATE STATUS:", update_response.status_code)
    print("UPDATE RESPONSE:", update_response.json())

    assert update_response.status_code == 200

    data = update_response.json()

    # -------------------------
    # Verify updated sale
    # -------------------------
    assert data["id"] == sale_id
    assert data["invoice_number"] == "UPDATE-SALE-002"
    assert data["customer_name"] == "Updated Customer"

    assert len(data["items"]) == 1

    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 3
    assert data["items"][0]["unit_price"] == 600

    assert data["total_amount"] == 1800
    
    
def test_delete_sale(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # -------------------------
    # Create category
    # -------------------------
    category_response = client.post(
        "/category/create",
        json={
            "name": "Delete Sale Category",
            "description": "Testing delete sale"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # -------------------------
    # Create product
    # -------------------------
    product_response = client.post(
        "/product/create",
        json={
            "name": "Delete Sale Product",
            "description": "Testing delete sale",
            "sku": "DELETE-SALE-001",
            "price": 500,
            "quantity": 20,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # -------------------------
    # Create sale
    # -------------------------
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "DELETE-SALE-001",
            "customer_name": "Delete Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    assert sale_response.status_code == 201

    sale_id = sale_response.json()["id"]

    # -------------------------
    # Delete sale as Admin
    # -------------------------
    delete_response = client.delete(
        f"/sales/delete/{sale_id}",
        headers=admin_headers
    )

    assert delete_response.status_code == 204

    # -------------------------
    # Verify sale is deleted
    # -------------------------
    get_response = client.get(
        f"/sales/sales/{sale_id}",
        headers=sales_headers
    )

    assert get_response.status_code == 404
    
    
def test_create_sale_invalid_product(
    client,
    sales_executive_token
):
    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # -------------------------
    # Create sale with invalid product
    # -------------------------
    sale_payload = {
        "invoice_number": "INVALID-PRODUCT-001",
        "customer_name": "Invalid Product Customer",
        "sale_date": "2026-08-12",
        "items": [
            {
                "product_id": 999999,
                "quantity": 2,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/sales/",
        json=sale_payload,
        headers=sales_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    # Product does not exist
    assert response.status_code == 404
    
    
def test_sale_decreases_stock(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # -------------------------
    # Create category as Admin
    # -------------------------
    category_response = client.post(
        "/category/create",
        json={
            "name": "Stock Sale Category",
            "description": "Testing stock decrease"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # -------------------------
    # Create product
    # Initial stock = 10
    # -------------------------
    product_response = client.post(
        "/product/create",
        json={
            "name": "Stock Sale Product",
            "description": "Testing stock decrease",
            "sku": "STOCK-SALE-001",
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
    # Create sale
    # Sale quantity = 3
    # -------------------------
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "SALE-STOCK-001",
            "customer_name": "Stock Test Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    assert sale_response.status_code == 201

    sale_data = sale_response.json()

    # Verify sale
    assert len(sale_data["items"]) == 1
    assert sale_data["items"][0]["product_id"] == product_id
    assert sale_data["items"][0]["quantity"] == 3
    assert sale_data["items"][0]["unit_price"] == 500

    # -------------------------
    # Get product after sale
    # Your product route is:
    # /product/product/{product_id}
    # -------------------------
    product_response = client.get(
        f"/product/product/{product_id}",
        headers=sales_headers
    )

    print("PRODUCT STATUS:", product_response.status_code)
    print("PRODUCT RESPONSE:", product_response.json())

    assert product_response.status_code == 200

    product_data = product_response.json()

    # -------------------------
    # Verify stock decreased
    # 10 - 3 = 7
    # -------------------------
    assert product_data["quantity"] == 7
    
    
def test_sale_insufficient_stock(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Insufficient Stock Category",
            "description": "Testing insufficient stock"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product with only 5 stock
    product_response = client.post(
        "/product/create",
        json={
            "name": "Low Stock Product",
            "description": "Testing insufficient stock",
            "sku": "LOW-STOCK-SALE-001",
            "price": 500,
            "quantity": 5,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Try to sell 10 when only 5 are available
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "INSUFFICIENT-STOCK-001",
            "customer_name": "Test Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 10,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    print("STATUS:", sale_response.status_code)
    print("RESPONSE:", sale_response.json())

    # Should be rejected
    assert sale_response.status_code in [400, 409]

    # Verify stock remains unchanged
    product_response = client.get(
        f"/product/product/{product_id}",
        headers=sales_headers
    )

    assert product_response.status_code == 200
    assert product_response.json()["quantity"] == 5
    
    
def test_create_sale_invalid_product(
    client,
    sales_executive_token
):
    headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    sale_payload = {
        "invoice_number": "INVALID-PRODUCT-001",
        "customer_name": "Test Customer",
        "sale_date": "2026-08-12",
        "items": [
            {
                "product_id": 999999,
                "quantity": 2,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/sales/",
        json=sale_payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code in [400, 404]
    
    
def test_create_sale_invalid_quantity(
    
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Invalid Sale Quantity Category",
            "description": "Testing invalid sale quantity"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Invalid Sale Quantity Product",
            "description": "Testing invalid sale quantity",
            "sku": "INVALID-SALE-QTY-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # Try to create sale with quantity = 0
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "INVALID-SALE-QTY-001",
            "customer_name": "Test Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 0,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    print("STATUS:", sale_response.status_code)
    print("RESPONSE:", sale_response.json())

    # Pydantic Field(gt=0) should reject quantity 0
    assert sale_response.status_code == 422
    
    
    
def test_create_sale_invalid_unit_price(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Invalid Sale Price Category",
            "description": "Testing invalid sale unit price"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Invalid Sale Price Product",
            "description": "Testing invalid sale unit price",
            "sku": "INVALID-SALE-PRICE-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # Try to create sale with unit_price = 0
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "INVALID-SALE-PRICE-001",
            "customer_name": "Test Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": 0
                }
            ]
        },
        headers=sales_headers
    )

    print("STATUS:", sale_response.status_code)
    print("RESPONSE:", sale_response.json())

    # Pydantic Field(gt=0) should reject unit_price = 0
    assert sale_response.status_code == 422
    
    
    
def test_inventory_manager_cannot_create_sale(
    client,
    inventory_manager_token
):
    headers = {
        "Authorization": f"Bearer {inventory_manager_token}"
    }

    sale_payload = {
        "invoice_number": "MANAGER-SALE-001",
        "customer_name": "Test Customer",
        "sale_date": "2026-08-12",
        "items": [
            {
                "product_id": 999999,
                "quantity": 1,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/sales/",
        json=sale_payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 403
    
    
def test_unauthenticated_cannot_create_sale(client):

    sale_payload = {
        "invoice_number": "UNAUTH-SALE-001",
        "customer_name": "Test Customer",
        "sale_date": "2026-08-12",
        "items": [
            {
                "product_id": 999999,
                "quantity": 1,
                "unit_price": 500
            }
        ]
    }

    response = client.post(
        "/sales/",
        json=sale_payload
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 401
    
    
    
def test_sales_executive_can_create_sale(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Sales Role Category",
            "description": "Testing sales role authorization"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Sales Role Product",
            "description": "Testing sales role authorization",
            "sku": "SALES-ROLE-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Sales Executive creates sale
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "SALES-ROLE-001",
            "customer_name": "Sales Role Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    print("STATUS:", sale_response.status_code)
    print("RESPONSE:", sale_response.json())

    assert sale_response.status_code == 201

    data = sale_response.json()

    assert data["customer_name"] == "Sales Role Customer"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 2
    
def test_sales_executive_cannot_delete_sale(
    client,
    admin_token,
    sales_executive_token
):
    admin_headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    sales_headers = {
        "Authorization": f"Bearer {sales_executive_token}"
    }

    # Create category
    category_response = client.post(
        "/category/create",
        json={
            "name": "Delete Authorization Category",
            "description": "Testing delete authorization"
        },
        headers=admin_headers
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create product
    product_response = client.post(
        "/product/create",
        json={
            "name": "Delete Authorization Product",
            "description": "Testing delete authorization",
            "sku": "DELETE-AUTH-001",
            "price": 500,
            "quantity": 10,
            "category_id": category_id
        },
        headers=admin_headers
    )

    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Create sale as Sales Executive
    sale_response = client.post(
        "/sales/",
        json={
            "invoice_number": "DELETE-AUTH-SALE-001",
            "customer_name": "Delete Auth Customer",
            "sale_date": "2026-08-12",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1,
                    "unit_price": 500
                }
            ]
        },
        headers=sales_headers
    )

    assert sale_response.status_code == 201

    sale_id = sale_response.json()["id"]

    # Sales Executive tries to delete sale
    delete_response = client.delete(
        f"/sales/delete/{sale_id}",
        headers=sales_headers
    )

    print("STATUS:", delete_response.status_code)
    print("RESPONSE:", delete_response.json())

    # Only Admin can delete
    assert delete_response.status_code == 403
    