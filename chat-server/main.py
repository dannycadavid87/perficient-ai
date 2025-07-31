from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, chats
import json

app = FastAPI(
    title="Chat Application Backend",
    description="FastAPI backend for chat application with JWT authentication and PostgreSQL",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "User registration, login, profile, and session management."},
        {"name": "Chats", "description": "Chat and message management."}
    ]
)

# Carga la base de conocimiento al iniciar
with open("kb/kb_computers.json", encoding="utf-8") as f:
    KB = json.load(f)

def retrieve_context(query: str):
    # Recupera la respuesta más relevante (simulación simple)
    for entry in KB:
        if any(word in query.lower() for word in entry["question"].lower().split()):
            return entry["answer"]
    return None

def generate_answer(query: str, context: str):
    # Simula la generación de respuesta usando contexto
    if context:
        return f"context: {context}\n\n'{query}', I couldn't find any relevant information in the knowledge base for your question."
    else:
        return f"I couldn't find any relevant information in the knowledge base for your question. '{query}'."

@app.get("/")
def read_root():
    return {"message": "Chat API working!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "")
    context = retrieve_context(query)
    answer = generate_answer(query, context)
    return {"answer": answer}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(chats.router)
