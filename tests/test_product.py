def test_create_product(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category first
    category_payload = {
        "name": "Test Electronics",
        "description": "Category for product testing"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_payload = {
        "name": "Test Laptop",
        "description": "Laptop for testing",
        "sku": "TEST-LAP-001",
        "price": 50000,
        "quantity": 10,
        "category_id": category_id
    }

    response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Laptop"
    assert data["sku"] == "TEST-LAP-001"
    assert data["price"] == 50000
    assert data["quantity"] == 10
    assert data["category_id"] == category_id
    
    
def test_get_all_products(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/product/all_products",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    
    
    
def test_get_product_by_id(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category
    category_payload = {
        "name": "Test Category For Get",
        "description": "Category for product test"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_payload = {
        "name": "Test Phone",
        "description": "Phone for testing",
        "sku": "TEST-PHONE-001",
        "price": 25000,
        "quantity": 5,
        "category_id": category_id
    }

    create_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    # Get product by ID
    response = client.get(
        f"/product/product/{product_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Test Phone"
    assert data["sku"] == "TEST-PHONE-001"
    assert data["price"] == 25000
    assert data["quantity"] == 5
    assert data["category_id"] == category_id
    
    
def test_update_product(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category
    category_payload = {
        "name": "Update Test Category",
        "description": "Category for update test"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_payload = {
        "name": "Old Product",
        "description": "Old description",
        "sku": "UPDATE-TEST-001",
        "price": 1000,
        "quantity": 10,
        "category_id": category_id
    }

    create_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    # Update product
    update_payload = {
        "name": "Updated Product",
        "description": "Updated description",
        "sku": "UPDATE-TEST-001",
        "price": 2000,
        "quantity": 20,
        "category_id": category_id
    }

    response = client.put(
        f"/product/update/product/{product_id}",
        json=update_payload,
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Updated Product"
    assert data["description"] == "Updated description"
    assert data["price"] == 2000
    assert data["quantity"] == 20
    
    
def test_delete_product(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category
    category_payload = {
        "name": "Delete Test Category",
        "description": "Category for delete test"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_payload = {
        "name": "Delete Test Product",
        "description": "Product to delete",
        "sku": "DELETE-TEST-001",
        "price": 500,
        "quantity": 5,
        "category_id": category_id
    }

    create_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    # Delete product
    response = client.delete(
        f"/product/delete/product/{product_id}",
        headers=headers
    )

    assert response.status_code == 204

    # Verify product no longer exists
    get_response = client.get(
        f"/product/product/{product_id}",
        headers=headers
    )

    assert get_response.status_code == 404
    
    
    
def test_create_product_duplicate_sku(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category
    category_payload = {
        "name": "Duplicate SKU Category",
        "description": "Category for duplicate SKU test"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    product_payload = {
        "name": "Product One",
        "description": "First product",
        "sku": "DUPLICATE-SKU-001",
        "price": 1000,
        "quantity": 10,
        "category_id": category_id
    }

    # First product
    first_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert first_response.status_code == 201

    # Second product with same SKU
    second_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Product SKU already exists"
    
    
    
def test_create_product_invalid_category(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    product_payload = {
        "name": "Invalid Category Product",
        "description": "Product with invalid category",
        "sku": "INVALID-CATEGORY-001",
        "price": 1000,
        "quantity": 10,
        "category_id": 999999
    }

    response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert response.status_code in [400, 404, 409]
    

def test_create_product_unauthorized(client):

    product_payload = {
        "name": "Unauthorized Product",
        "description": "Should not be created",
        "sku": "UNAUTHORIZED-001",
        "price": 1000,
        "quantity": 10,
        "category_id": 1
    }

    response = client.post(
        "/product/create",
        json=product_payload
    )

    assert response.status_code in [401, 403]
    
    
    
def test_update_product_unauthorized(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category
    category_payload = {
        "name": "Unauthorized Update Category",
        "description": "Category for authorization test"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_payload = {
        "name": "Original Product",
        "description": "Original description",
        "sku": "UNAUTHORIZED-UPDATE-001",
        "price": 1000,
        "quantity": 10,
        "category_id": category_id
    }

    create_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    # Try updating without authentication
    update_payload = {
        "name": "Hacked Product",
        "description": "Should not update",
        "sku": "UNAUTHORIZED-UPDATE-001",
        "price": 5000,
        "quantity": 100,
        "category_id": category_id
    }

    response = client.put(
        f"/product/update/product/{product_id}",
        json=update_payload
    )

    assert response.status_code in [401, 403]
    
    
def test_delete_product_unauthorized(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create category
    category_payload = {
        "name": "Unauthorized Delete Category",
        "description": "Category for authorization test"
    }

    category_response = client.post(
        "/category/create",
        json=category_payload,
        headers=headers
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create product
    product_payload = {
        "name": "Delete Protected Product",
        "description": "Should not be deleted",
        "sku": "UNAUTHORIZED-DELETE-001",
        "price": 1000,
        "quantity": 10,
        "category_id": category_id
    }

    create_response = client.post(
        "/product/create",
        json=product_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    # Try deleting without authentication
    response = client.delete(
        f"/product/delete/product/{product_id}"
    )

    assert response.status_code in [401, 403]