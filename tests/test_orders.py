from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_create_order_success():
    response = client.post("/orders", json={
        "customer_name": "John Doe",
        "phone": "1234567890",
        "garments": [{"type": "Shirt", "quantity": 2}, {"type": "Pants", "quantity": 1}]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["phone"] == "1234567890"
    assert data["status"] == "RECEIVED"
    assert "order_id" in data

def test_invalid_phone():
    response = client.post("/orders", json={
        "customer_name": "John Doe",
        "phone": "123", # Invalid phone
        "garments": [{"type": "Shirt", "quantity": 2}]
    })
    assert response.status_code == 422

def test_empty_garments():
    response = client.post("/orders", json={
        "customer_name": "John Doe",
        "phone": "1234567890",
        "garments": [] # Empty garments
    })
    assert response.status_code == 422

def test_status_update():
    # First create an order
    create_response = client.post("/orders", json={
        "customer_name": "Jane Smith",
        "phone": "0987654321",
        "garments": [{"type": "Saree", "quantity": 1}]
    })
    assert create_response.status_code == 201
    order_id = create_response.json()["order_id"]
    
    # Update status to PROCESSING
    update_response = client.patch(f"/orders/{order_id}/status", json={
        "status": "PROCESSING"
    })
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "PROCESSING"

def test_status_update_invalid():
    # Attempt to use invalid status
    create_response = client.post("/orders", json={
        "customer_name": "Jane Smith",
        "phone": "0987654321",
        "garments": [{"type": "Saree", "quantity": 1}]
    })
    order_id = create_response.json()["order_id"]
    
    update_response = client.patch(f"/orders/{order_id}/status", json={
        "status": "NOT_A_STATUS"
    })
    assert update_response.status_code == 422
