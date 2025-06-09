import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

with open("faq_data.json", "r") as f:
    faqs = json.load(f)

model = genai.GenerativeModel(model_name="models/chat-bison-001")

def get_answer(user_question):
    context = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])
    prompt = f"""
You are a helpful assistant. Use the following FAQ context to answer:
{context}
User Question: {user_question}
Answer:
"""
    response = model.generate_content(prompt)
    return response.text.strip()
