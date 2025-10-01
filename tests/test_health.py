# PYTHONPATH=. pytest -v

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

def test_get_search_no_query():
    resp = client.get("/search")
    assert resp.status_code == 200
    data = resp.json()
    # Expect a list (because GET /search returns list of Video or empty list)
    assert isinstance(data, list)

def test_get_search_with_query():
    resp = client.get("/search?q=Kubernetes")
    assert resp.status_code == 200
    data = resp.json()
    # Since the mock data includes “Kubernetes Basics”, it should appear
    assert any("Kubernetes" in vid["title"] for vid in data)

def test_post_search_not_implemented():
    resp = client.post("/search", json={})
    assert resp.status_code in (200, 405, 501)  # depending on your stub setup
    # Better: enforce 200 and body detail
    assert resp.json() == {"detail": "Not implemented"}

def test_put_search_not_implemented():
    resp = client.put("/search/1", json={})
    assert resp.status_code in (200, 405, 501)
    # If the stub returns detail string with video_id
    assert resp.json()["detail"].startswith("Not implemented")

def test_delete_search_not_implemented():
    resp = client.delete("/search/1")
    assert resp.status_code in (200, 405, 501)
    assert resp.json()["detail"].startswith("Not implemented")
