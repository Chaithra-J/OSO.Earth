# app/main.py
import os
from app.chatbot import answer_question
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
PDF_DIR = os.path.join(BASE_DIR, "app", "pdfs")

# from chatbot import answer_question

app = FastAPI(title="OSO Chatbot")

# Allow frontend (adjust CORS in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    # path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    # return FileResponse(path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
    

@app.post("/ask")
async def ask(payload: dict):
    question = payload.get("question", "").strip()
    if not question:
        return JSONResponse({"error": "Empty question"}, status_code=400)
    result = answer_question(question)
    return result

@app.get("/pdfs/{filename}")
def serve_pdf(filename: str):
    path = os.path.join(PDF_DIR, filename)
    if not os.path.isfile(path):
        return JSONResponse({"error": "file not found"}, status_code=404)
    return FileResponse(path, media_type="application/pdf")
