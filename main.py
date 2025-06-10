from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import time
from gemini_utils import get_answer
from feedback_store import store_feedback
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FAQ Chatbot", version="1.0")
templates = Jinja2Templates(directory="templates")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    user_feedback: str

def is_coding_question(question: str) -> bool:
    keywords = [
        "python", "java", "c++", "javascript", "code", "program", "algorithm",
        "function", "variable", "bug", "error", "compile", "run", "syntax",
        "loop", "array", "list", "dictionary", "class", "object", "method",
        "sql", "database", "html", "css", "react", "django", "flask", "api"
    ]
    q = question.lower()
    return any(word in q for word in keywords)

def is_greeting(question):
    greetings = ["hi", "hello", "hey"]
    return question.strip().lower() in greetings

def store_qa_for_learning(question, answer, filename="learned_qa.json"):
    """Append Q&A to a JSON file for self-learning."""
    data = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    data.append({"question": question, "answer": answer})
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Render the main chat interface"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "question": "",
            "answer": "",
            "history": []
        }
    )

@app.post("/ask", response_class=HTMLResponse)
async def handle_question(
    request: Request,
    question: str = Form(...),
    history: str = Form("[]")
):
    try:
        logger.info(f"Processing question: {question}")
        if is_greeting(question):
            answer = "Hello! 👋 How can I assist you with your coding questions today?"
        elif not is_coding_question(question):
            answer = "I'm not able to answer non-coding questions."
        else:
            answer = get_answer(question)
        chat_history = json.loads(history)
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "bot", "content": answer})
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "question": "",
                "answer": answer,
                "history": chat_history
            }
        )
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "question": "",
                "answer": f"Error: {str(e)}",
                "history": json.loads(history)
            },
            status_code=500
        )

@app.post("/api/ask")
async def api_ask_question(payload: AskRequest):
    """API endpoint for programmatic access"""
    try:
        if not is_coding_question(payload.question):
            answer = "I'm not able to answer non-coding questions."
        else:
            answer = get_answer(payload.question)
        return JSONResponse({
            "question": payload.question,
            "answer": answer
        })
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def submit_feedback(payload: FeedbackRequest):
    """Handle user feedback"""
    try:
        # You can use feedback here to improve answer style in the future
        store_feedback(
            payload.question,
            payload.answer,
            payload.user_feedback
        )
        return {"status": "success", "message": "Feedback recorded"}
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": app.version}