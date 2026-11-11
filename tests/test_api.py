from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_root():
 r=client.get("/"); assert r.status_code==200 and r.json()["status"]=="operational"
def test_health():
 r=client.get("/healthz"); assert r.status_code==200 and r.json()=={"status":"ok"}
def test_info():
 r=client.get("/api/v1/info"); assert r.status_code==200 and "build_sha" in r.json()
def test_resources():
 r=client.get("/api/v1/resources"); assert r.status_code==200 and r.json()["count"]==5
def test_resource():
 r=client.get("/api/v1/resources/github"); assert r.status_code==200 and r.json()["name"]=="GitHub"
def test_missing_resource():
 r=client.get("/api/v1/resources/missing"); assert r.status_code==404
def test_echo_valid():
 r=client.post("/api/v1/echo",json={"message":"hello"}); assert r.status_code==200 and r.json()["received"] is True
def test_echo_invalid():
 r=client.post("/api/v1/echo",json={"message":""}); assert r.status_code==422
def test_security_headers():
 r=client.get("/healthz"); assert r.headers["X-Content-Type-Options"]=="nosniff" and "X-Request-ID" in r.headers
