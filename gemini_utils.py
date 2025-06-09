# import google.generativeai as genai
# import os
# import json
# from dotenv import load_dotenv
# from PIL import Image

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# with open("faq_data.json", "r") as f:
#     faqs = json.load(f)

# # Use the new Gemini model
# model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# def get_answer(user_question, image_path=None):
#     context = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])
#     prompt = f"""
# You are a helpful assistant. Use the following FAQ context to answer:
# {context}
# User Question: {user_question}
# Answer:
# """.strip()

#     # If image is provided
#     if image_path:
#         img = Image.open(image_path)
#         response = model.generate_content([prompt, img])
#     else:
#         response = model.generate_content([prompt])  # Still pass as list

#     return response.text.strip()



import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_answer(user_question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # Use your Groq model here
        "messages": [
            {
                "role": "user",
                "content": user_question
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        # Extract the assistant's reply from the response JSON
        return data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage:
question = "Explain the importance of fast language models"
print(get_answer(question))
