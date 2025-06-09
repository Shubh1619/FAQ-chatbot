import json
import os

feedback_file = "feedback.json"

def store_feedback(question, answer, user_feedback):
    feedback_entry = {
        "question": question,
        "answer": answer,
        "user_feedback": user_feedback
    }

    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(feedback_entry)

    with open(feedback_file, "w") as f:
        json.dump(data, f, indent=4)