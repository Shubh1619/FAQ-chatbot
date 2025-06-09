from fastapi import FastAPI, Request
from gemini_utils import get_answer
from feedback_store import store_feedback

app = FastAPI()

@app.post("/ask")
async def ask_question(req: Request):
    data = await req.json()
    question = data["question"]
    answer = get_answer(question)
    return {"question": question, "answer": answer}

@app.post("/feedback")
async def feedback(req: Request):
    data = await req.json()
    store_feedback(data["question"], data["answer"], data["user_feedback"])
    return {"message": "Feedback saved successfully."}