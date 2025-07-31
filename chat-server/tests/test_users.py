import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    client.post("/users/login", json={"username": "testuser", "email": "test@example.com", "password": "testpass"})
    response = client.post("/users/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_without_username():
    client.post("/users/login", json={"email": "test@example.com", "password": "testpass"})
    response = client.post("/users/login", data={"password": "testpass"})
    assert response.status_code == 422  # Unprocessable Entity

def test_login_without_password():
    client.post("/users/login", json={"username": "testuser2", "email": "test2@example.com"})
    response = client.post("/users/login", data={"username": "testuser2"})
    assert response.status_code == 422  # Unprocessable Entity

def test_login_with_invalid_credentials():
    client.post("/users/login", json={"username": "testuser2", "email": "test@example.com", "password": "testpass"})
    response = client.post("/users/login", data={"username": "invaliduser", "password": "wrongpass"})
    assert response.status_code == 401  # Unauthorized
