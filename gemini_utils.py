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
import json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Replace 'groq' with the actual SDK package if it exists
try:
    import groq  # assuming actual SDK is named groq
except ImportError:
    raise ImportError("Groq SDK not installed. Please run: pip install groq")

# Initialize client with API key only
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

with open("faq_data.json", "r") as f:
    faqs = json.load(f)

def get_answer(user_question, image_path=None):
    context = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])
    prompt = f"""
You are a helpful assistant. Use the following FAQ context to answer:
{context}
User Question: {user_question}
Answer:
""".strip()

    if image_path:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
        # Assuming the client has a method to handle vision+text inputs
        response = client.generate(
            model="vision-model",
            inputs={"text": prompt, "image_bytes": img_bytes}
        )
    else:
        response = client.generate(
            model="text-model",
            inputs={"text": prompt}
        )

    # Adjust depending on SDK response format
    return response.text if hasattr(response, 'text') else response.get('text', '')

