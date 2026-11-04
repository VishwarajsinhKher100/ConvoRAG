# backend/src/backend/main.py (Updated sections)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import chat, auth, rag
from .telemetry import init_telemetry  # <--- Import telemetry setup

# Create tables in PostgreSQL if they don't already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot API")

# Initialize Production Logging & Prometheus Monitoring
init_telemetry(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "Chatbot API is running"}

# Include routers
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(rag.router)