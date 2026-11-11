from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_service_metadata():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "CloudOps Deployment API"
    assert body["status"] == "operational"
    assert body["links"]["documentation"] == "/docs"


def test_health_endpoint_is_successful():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info_endpoint_exposes_build_metadata_without_secrets():
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.0.0"
    assert "build_sha" in body
    assert "environment" in body
    assert "secret" not in body


def test_resource_collection_returns_expected_items():
    response = client.get("/api/v1/resources")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 5
    assert any(item["id"] == "cloud-run" for item in body["items"])


def test_single_resource_can_be_retrieved():
    response = client.get("/api/v1/resources/github")
    assert response.status_code == 200
    assert response.json()["name"] == "GitHub"


def test_unknown_resource_returns_404():
    response = client.get("/api/v1/resources/not-a-real-resource")
    assert response.status_code == 404
    assert response.json() == {"detail": "Resource not found"}


def test_echo_post_accepts_valid_json():
    response = client.post(
        "/api/v1/echo",
        json={"message": "deployment validation", "correlation_id": "postman-001"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "received": True,
        "message": "deployment validation",
        "correlation_id": "postman-001",
    }


def test_echo_post_rejects_invalid_empty_message():
    response = client.post("/api/v1/echo", json={"message": ""})
    assert response.status_code == 422


def test_security_headers_are_present():
    response = client.get("/healthz")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "X-Request-ID" in response.headers
