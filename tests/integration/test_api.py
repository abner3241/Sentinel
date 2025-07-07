import pytest
from fastapi.testclient import TestClient
from core.app import app

client = TestClient(app)

def test_status_endpoint():
    res = client.get("/status")
    assert res.status_code == 200
    assert "status" in res.json()
