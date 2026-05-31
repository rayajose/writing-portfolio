import sys
import os
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from main import app

client = TestClient(app)

HEADERS = {"x-api-key": "demo-secret-key"}


def test_list_products():
    response = client.get(
        "/products?limit=10&sort_by=product_id&order=asc",
        headers=HEADERS,
    )

    assert response.status_code == 200

    body = response.json()
    assert "count" in body
    assert "items" in body
    assert isinstance(body["items"], list)
