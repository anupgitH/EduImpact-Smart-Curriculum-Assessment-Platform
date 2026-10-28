from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
def test_courses_requires_auth():
    assert client.get("/api/v1/courses").status_code == 401
