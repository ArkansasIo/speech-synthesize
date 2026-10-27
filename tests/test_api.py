from fastapi.testclient import TestClient
from speech_synthesize.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_empty_text_is_rejected() -> None:
    response = client.post("/v1/synthesize", json={"text": ""})
    assert response.status_code == 422


def test_rate_out_of_range_is_rejected() -> None:
    response = client.post("/v1/synthesize", json={"text": "Hello", "rate": 999})
    assert response.status_code == 422
