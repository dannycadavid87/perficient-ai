import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    client.post("/users/register", json={"username": "msguser", "email": "msg@example.com", "password": "testpass"})
    response = client.post("/users/login", data={"username": "msguser", "password": "testpass"})
    return response.json()["access_token"]

def test_send_message():
    token = get_token()
    chat_resp = client.post("/chats/", json={"title": "Msg Chat"}, headers={"Authorization": f"Bearer {token}"})
    chat_id = chat_resp.json()["id"]
    response = client.post(f"/chats/{chat_id}/messages", json={"content": "Hello!"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["content"] == "Hello!"
