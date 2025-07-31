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

def test_send_message_missing_content():
    token = get_token()
    chat_resp = client.post("/chats/", json={"title": "Test Chat"}, headers={"Authorization": f"Bearer {token}"})
    chat_id = chat_resp.json()["id"]
    response = client.post(f"/chats/{chat_id}/messages", json={}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"  # Depending on how FastAPI handles it

def test_send_message_Question1():
    token = get_token()
    chat_resp = client.post("/chats/", json={"title": "What is more important, more RAM or a better processor?"}, headers={"Authorization": f"Bearer {token}"})
    chat_id = chat_resp.json()["id"]
    response = client.post(f"/chats/{chat_id}/messages", json={"It depends on your needs. More RAM helps with multitasking and web browsing, while a better processor is crucial for gaming, video editing, and demanding applications."}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["content"] == "It depends on your needs. More RAM helps with multitasking and web browsing, while a better processor is crucial for gaming, video editing, and demanding applications."

def test_send_message_Question2():
    token = get_token()
    chat_resp = client.post("/chats/", json={"title": "What does SSD mean?"}, headers={"Authorization": f"Bearer {token}"})
    chat_id = chat_resp.json()["id"]
    response = client.post(f"/chats/{chat_id}/messages", json={"content": "SSD stands for Solid State Drive. It is a type of storage that is much faster and more reliable than traditional hard disk drives (HDD)."}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["content"] == "SSD stands for Solid State Drive. It is a type of storage that is much faster and more reliable than traditional hard disk drives (HDD)."

def test_send_message_Question3():
    token = get_token()
    chat_resp = client.post("/chats/", json={"title": "Which computer is better for gaming?"}, headers={"Authorization": f"Bearer {token}"})
    chat_id = chat_resp.json()["id"]
    response = client.post(f"/chats/{chat_id}/messages", json={"content": "For gaming, look for a computer with a powerful graphics card (GPU), a fast processor, and at least 16GB of RAM."}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["content"] == "For gaming, look for a computer with a powerful graphics card (GPU), a fast processor, and at least 16GB of RAM."
