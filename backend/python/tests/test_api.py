import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_main_redirect():
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"

def test_get_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_signup_recruiter():
    signup_data = {
        "table": "recruiters",
        "data": {
            "company_name": "Test Company",
            "phone_number": "1234567890",
            "state": "Test State",
            "city_or_province": "Test City",
            "zip_code": "12345",
            "email": "test@example.com",
            "password": "testpassword"
        }
    }
    response = client.post("/signup", json=signup_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Recruiter signed up successfully"}

# Add more tests for other endpoints and edge cases
