from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, chats

app = FastAPI(
    title="Chat Application Backend",
    description="FastAPI backend for chat application with JWT authentication and PostgreSQL",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "User registration, login, profile, and session management."},
        {"name": "Chats", "description": "Chat and message management."}
    ]
)

@app.get("/")
def read_root():
    return {"message": "API de chat funcionando"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(chats.router)
