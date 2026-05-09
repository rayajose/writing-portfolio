import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from main import app

client = TestClient(app)

HEADERS = {"x-api-key": "demo-secret-key"}


def test_create_order():
    response = client.post(
        "/orders",
        headers=HEADERS,
        json={
            "partner_name": "RayTech Corp.",
            "customer_reference": "TEST-ORDER-001",
            "items": [
                {
                    "product_id": "PR00001",
                    "quantity": 1,
                }
            ],
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["order_id"].startswith("OR")
    assert body["status"] == "created"
    assert len(body["items"]) == 1