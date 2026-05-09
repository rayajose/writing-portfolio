import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from main import app

client = TestClient(app)

HEADERS = {"x-api-key": "demo-secret-key"}


def test_sales_by_partner():
    response = client.get(
        "/analytics/sales-by-partner",
        headers=HEADERS,
    )

    assert response.status_code == 200

    body = response.json()
    assert "analytics_type" in body
    assert "results" in body


def test_sales_over_time():
    response = client.get(
        "/analytics/sales-over-time?grain=daily",
        headers=HEADERS,
    )

    assert response.status_code == 200

    body = response.json()
    assert "analytics_type" in body
    assert "results" in body


def test_revenue_share():
    response = client.get(
        "/analytics/revenue-share",
        headers=HEADERS,
    )

    assert response.status_code == 200

    body = response.json()
    assert "analytics_type" in body
    assert "results" in body