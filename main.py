from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import time
from gemini_utils import get_answer
from feedback_store import store_feedback
import logging

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
    session_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    user_feedback: str
    session_id: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Render the main chat interface"""
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "question": "",
            "answer": "",
            "session_id": str(int(time.time()))
        }
    )

@app.post("/ask", response_class=HTMLResponse)
async def handle_question(
    request: Request,
    question: str = Form(...),
    session_id: str = Form(...)
):
    """Handle question submission from the chat interface"""
    try:
        logger.info(f"Processing question from session {session_id}: {question}")
        answer = get_answer(question)
        return templates.TemplateResponse(
            "chat.html",
            {
                "request": request,
                "question": question,
                "answer": answer,
                "session_id": session_id
            }
        )
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return templates.TemplateResponse(
            "chat.html",
            {
                "request": request,
                "question": question,
                "answer": f"Error: {str(e)}",
                "session_id": session_id
            },
            status_code=500
        )

@app.post("/api/ask")
async def api_ask_question(payload: AskRequest):
    """API endpoint for programmatic access"""
    try:
        answer = get_answer(payload.question)
        return JSONResponse({
            "question": payload.question,
            "answer": answer,
            "session_id": payload.session_id
        })
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def submit_feedback(payload: FeedbackRequest):
    """Handle user feedback"""
    try:
        store_feedback(
            payload.question,
            payload.answer,
            payload.user_feedback,
            payload.session_id
        )
        return {"status": "success", "message": "Feedback recorded"}
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": app.version}