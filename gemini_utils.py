import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load your FAQ data
with open("faq_data.json", "r") as f:
    faqs = json.load(f)

# Function to generate answer
def get_answer(user_question, image_path=None):
    context = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])

    prompt = f"""
You are a helpful assistant. Use the following FAQ context to answer:
{context}

User Question: {user_question}
Answer:
"""

    if image_path:
        # Use vision model if image is provided
        model = genai.GenerativeModel(model_name="models/gemini-pro-vision")
        
        # Load image
        from PIL import Image
        img = Image.open(image_path)

        response = model.generate_content([prompt.strip(), img])
    else:
        # Use text-only model
        model = genai.GenerativeModel(model_name="models/gemini-pro")
        response = model.generate_content(prompt.strip())

    return response.text.strip()
