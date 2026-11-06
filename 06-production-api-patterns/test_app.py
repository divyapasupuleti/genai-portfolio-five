from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_complete_and_cache():
    payload = {"prompt": "hello ireland", "use_cache": True}
    r1 = client.post("/v1/complete", json=payload)
    assert r1.status_code == 200
    body1 = r1.json()
    assert body1["cached"] is False
    assert "trace_id" in body1

    r2 = client.post("/v1/complete", json=payload)
    body2 = r2.json()
    assert body2["cached"] is True
    assert body2["text"] == body1["text"]
