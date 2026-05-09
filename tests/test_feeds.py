import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from main import app

client = TestClient(app)

HEADERS = {"x-api-key": "demo-secret-key"}


def test_get_feed_not_found():
    response = client.get(
        "/feeds/FD99999",
        headers=HEADERS,
    )

    assert response.status_code == 404