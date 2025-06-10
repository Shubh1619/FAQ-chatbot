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


