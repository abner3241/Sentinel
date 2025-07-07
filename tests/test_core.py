import pytest
from core.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_status_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert "status" in response.json()
