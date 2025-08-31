from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_send_smoke():
    client = TestClient(app)
    payload = {
        "channel": "email",
        "to": ["dev@example.com"],
        "subject": "Hello",
        "body_text": "Hi",
        "idempotency_key": "test-1",
    }
    resp = client.post("/api/v1/notifications/send", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "queued"
    assert "task_id" in data
