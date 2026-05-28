import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from main import app

client = TestClient(app)

HEADERS = {"x-api-key": "demo-secret-key"}


def test_create_customer():
    response = client.post(
        "/customers",
        headers=HEADERS,
        json={
            "first_name": "Alex",
            "last_name": "Morgan",
            "email": "alex.morgan@example.com",
            "phone": "555-0101",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["customer_id"].startswith("CU")
    assert body["first_name"] == "Alex"
    assert body["last_name"] == "Morgan"
    assert body["email_masked"] == "al***@example.com"
    assert body["phone_masked"] == "***-***-0101"
    assert "email_encrypted" not in body
    assert "phone_encrypted" not in body


def test_create_customer_address():
    customer_response = client.post(
        "/customers",
        headers=HEADERS,
        json={
            "first_name": "Jordan",
            "last_name": "Lee",
            "email": "jordan.lee@example.com",
            "phone": "555-0102",
        },
    )

    assert customer_response.status_code == 201

    customer_id = customer_response.json()["customer_id"]

    address_response = client.post(
        f"/customers/{customer_id}/addresses",
        headers=HEADERS,
        json={
            "address_line1": "123 Example Street",
            "address_line2": "Apt 4B",
            "city": "Seattle",
            "state": "WA",
            "postal_code": "98101",
            "country": "US",
        },
    )

    assert address_response.status_code == 201

    body = address_response.json()
    assert body["address_id"].startswith("AD")
    assert body["customer_id"] == customer_id
    assert body["address_line1_masked"] == "123 ***"
    assert body["postal_code_masked"] == "***01"
    assert "address_line1_encrypted" not in body
    assert "postal_code_encrypted" not in body


def test_get_customers_returns_200():
    response = client.get(
        "/customers",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_orders_returns_200():
    response = client.get(
        "/customers/CU00021/orders",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
