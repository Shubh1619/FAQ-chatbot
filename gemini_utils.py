import os
import requests
from dotenv import load_dotenv
import re

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def is_code_question(question):
    code_keywords = [
        "write a program", "code", "implement", "function", "class", "script",
        "algorithm", "example", "show me", "how to", "python code", "c++ code",
        "java code", "javascript code", "give me code", "program"
    ]
    q = question.lower()
    return any(word in q for word in code_keywords)

def get_answer(user_question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Always prompt for code, not theory
    prompt = (
        "Write the complete Python code for the following request. "
        "Return only the code, with correct formatting and indentation. "
        "Do not wrap it in markdown or triple backticks. "
        "Do not add any explanation or comments. "
        "Just output the code as you would write it in a .py file:\n" + user_question
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"


