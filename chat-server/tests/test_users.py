import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    client.post("/users/register", json={"username": "testuser2", "email": "test2@example.com", "password": "testpass"})
    response = client.post("/users/login", data={"username": "testuser2", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
