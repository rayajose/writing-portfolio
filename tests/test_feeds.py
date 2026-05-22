from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_customers_returns_200():
    response = client.get(
        "/customers",
        headers={"x-api-key": "test-api-key"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_by_id_returns_200():
    response = client.get(
        "/customers/CU00001",
        headers={"x-api-key": "test-api-key"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == "CU00001"
    assert "email_masked" in data
    assert "phone_masked" in data
    assert "email_encrypted" not in data
    assert "phone_encrypted" not in data
