def test_create_supplier(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    supplier_payload = {
        "name": "Test Supplier",
        "company_name": "Test Supplies Pvt Ltd",
        "email": "supplier@test.com",
        "phone": "9876543210",
        "address": "Ludhiana, Punjab"
    }

    response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Supplier"
    assert data["company_name"] == "Test Supplies Pvt Ltd"
    assert data["email"] == "supplier@test.com"
    assert data["phone"] == "9876543210"
    assert data["address"] == "Ludhiana, Punjab"
    assert "id" in data
    
    
def test_get_all_suppliers(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create supplier
    supplier_payload = {
        "name": "Get All Supplier",
        "company_name": "Get All Supplies Pvt Ltd",
        "email": "getall@test.com",
        "phone": "9876543211",
        "address": "Ludhiana, Punjab"
    }

    create_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    # Get all suppliers
    response = client.get(
        "/supplier/all_suppliers",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    supplier = data[-1]

    assert supplier["name"] == "Get All Supplier"
    assert supplier["company_name"] == "Get All Supplies Pvt Ltd"
    
    
    
def test_get_supplier_by_id(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    supplier_payload = {
        "name": "Get By ID Supplier",
        "company_name": "Get By ID Supplies Pvt Ltd",
        "email": "getbyid_unique_001@test.com",
        "phone": "9876543299",
        "address": "Ludhiana, Punjab"
    }

    # Create supplier
    create_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    print("CREATE STATUS:", create_response.status_code)
    print("CREATE RESPONSE:", create_response.json())

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    # Get supplier by ID
    response = client.get(
        f"/supplier/supplier/{supplier_id}",
        headers=headers
    )

    print("GET STATUS:", response.status_code)
    print("GET RESPONSE:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == supplier_id
    assert data["name"] == supplier_payload["name"]
    assert data["company_name"] == supplier_payload["company_name"]
    assert data["email"] == supplier_payload["email"]
    assert data["phone"] == supplier_payload["phone"]
    assert data["address"] == supplier_payload["address"]
    
    
    
def test_update_supplier(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create supplier
    supplier_payload = {
        "name": "Old Supplier",
        "company_name": "Old Company",
        "email": "old@test.com",
        "phone": "9876543213",
        "address": "Ludhiana, Punjab"
    }

    create_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    # Update supplier
    update_payload = {
        "name": "Updated Supplier",
        "company_name": "Updated Company",
        "email": "updated@test.com",
        "phone": "9876543214",
        "address": "Mohali, Punjab"
    }

    response = client.put(
        f"/supplier/update/supplier/{supplier_id}",
        json=update_payload,
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == supplier_id
    assert data["name"] == "Updated Supplier"
    assert data["company_name"] == "Updated Company"
    assert data["email"] == "updated@test.com"
    assert data["phone"] == "9876543214"
    assert data["address"] == "Mohali, Punjab"
    
    
def test_delete_supplier(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create supplier
    supplier_payload = {
        "name": "Delete Supplier",
        "company_name": "Delete Company",
        "email": "delete@test.com",
        "phone": "9876543215",
        "address": "Ludhiana, Punjab"
    }

    create_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    # Delete supplier
    response = client.delete(
    f"/supplier/delete/supplier/{supplier_id}",
    headers=headers
)
    assert response.status_code == 200
    get_response = client.get(
    f"/supplier/supplier/{supplier_id}",
    headers=headers
)
    assert get_response.status_code == 404
    
    
    
def test_get_nonexistent_supplier(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.get(
        "/supplier/supplier/999999",
        headers=headers
    )

    assert response.status_code == 404
    
    
def test_update_nonexistent_supplier(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    update_payload = {
        "name": "Updated Supplier",
        "company_name": "Updated Company",
        "email": "updated@test.com",
        "phone": "9876543216",
        "address": "Mohali, Punjab"
    }

    response = client.put(
        "/supplier/update/supplier/999999",
        json=update_payload,
        headers=headers
    )

    assert response.status_code == 404
    
    
def test_delete_nonexistent_supplier(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.delete(
        "/supplier/delete/supplier/999999",
        headers=headers
    )

    assert response.status_code == 404


def test_create_supplier_without_auth(client):

    supplier_payload = {
        "name": "Unauthorized Supplier",
        "company_name": "Unauthorized Company",
        "email": "unauthorized@test.com",
        "phone": "9876543217",
        "address": "Ludhiana, Punjab"
    }

    response = client.post(
        "/supplier/create",
        json=supplier_payload
    )

    assert response.status_code in [401, 403]
    
    
def test_update_supplier_without_auth(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create supplier first
    supplier_payload = {
        "name": "Protected Supplier",
        "company_name": "Protected Company",
        "email": "protected@test.com",
        "phone": "9876543218",
        "address": "Ludhiana, Punjab"
    }

    create_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    # Try updating without authentication
    update_payload = {
        "name": "Unauthorized Update",
        "company_name": "Unauthorized Company",
        "email": "unauthorized-update@test.com",
        "phone": "9876543219",
        "address": "Mohali, Punjab"
    }

    response = client.put(
        f"/supplier/update/supplier/{supplier_id}",
        json=update_payload
    )

    assert response.status_code in [401, 403]
    
    
    
def test_delete_supplier_without_auth(client, admin_token):

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    # Create supplier first
    supplier_payload = {
        "name": "Protected Delete Supplier",
        "company_name": "Protected Delete Company",
        "email": "protected-delete@test.com",
        "phone": "9876543220",
        "address": "Ludhiana, Punjab"
    }

    create_response = client.post(
        "/supplier/create",
        json=supplier_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    supplier_id = create_response.json()["id"]

    # Try deleting without authentication
    response = client.delete(
        f"/supplier/delete/supplier/{supplier_id}"
    )

    assert response.status_code in [401, 403]