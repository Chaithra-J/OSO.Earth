from fastapi import FastAPI
from backend.memory import (
    get_habits,
    add_habit,
    complete_habit,
    user_context,
    delete_habit,
    get_user_habit_context,
    habit_context_to_text
)
from backend.llm import ask_llm
from backend.rag import get_vector_db, retrieve_pdf_context, retrieve_knowledge

app = FastAPI()

# Initialise Vector DB on startup
@app.on_event("startup")
def startup_event():
    try:
        get_vector_db()
    except Exception as e:
        print(f"Startup Warning: {e}")

@app.get("/habits")
def list_habits():
    return [{"id": h.id, "name": h.name, "streak": h.streak} for h in get_habits()]

@app.post("/habits/{name}")
def create_habit(name: str):
    add_habit(name)
    return {"status": "habit added"}

@app.post("/habits/{habit_id}/complete")
def mark_complete(habit_id: int):
    complete_habit(habit_id)
    return {"status": "habit completed"}

@app.delete("/habit/{habit_id}")
def remove_habit(habit_id: int):
    delete_habit(habit_id)
    return {"status": "deleted"}

@app.get("/chat")
def chat(message: str):
    # Use the grounded reasoning function
    response = answer_user_question(message)
    return {"response": response}

def answer_user_question(user_message):
    pdf_context, found = retrieve_pdf_context(user_message)

    if not found or len(pdf_context) < 10:
        return "I couldn't find relevant info in the documents to answer that."

    habit_ctx = get_user_habit_context()
    habit_text = habit_context_to_text(habit_ctx)

    prompt = f"""
You are a grounded Habit Coach. Answer using ONLY the PDF knowledge.

PDF knowledge:
\"\"\"
{pdf_context}
\"\"\"

User habit context:
\"\"\"
{habit_text}
\"\"\"

User question: {user_message}

Rules:
1. Ground answer in PDF.
2. If PDF doesn't have the info, say you don't know.
3. Suggest a habit only if logically relevant.
"""
    return ask_llm(prompt)
