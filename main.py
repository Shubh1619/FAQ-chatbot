from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_utils import get_answer
from feedback_store import store_feedback

app = FastAPI()

# Optional: Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema for /ask
class AskRequest(BaseModel):
    question: str

# Request schema for /feedback
class FeedbackRequest(BaseModel):
    question: str
    answer: str
    user_feedback: str

@app.post("/ask")
async def ask_question(payload: AskRequest):
    try:
        answer = get_answer(payload.question)
        return {"question": payload.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def feedback(payload: FeedbackRequest):
    try:
        store_feedback(payload.question, payload.answer, payload.user_feedback)
        return {"message": "Feedback saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
