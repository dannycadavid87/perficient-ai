import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    client.post("/users/register", json={"username": "chatuser", "email": "chat@example.com", "password": "testpass"})
    response = client.post("/users/login", data={"username": "chatuser", "password": "testpass"})
    return response.json()["access_token"]

def test_create_chat():
    token = get_token()
    response = client.post("/chats/", json={"title": "Test Chat"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Chat"
