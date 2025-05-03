from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Function to interact with an AI API
def get_ai_response(user_question):
    """Fetch AI-generated answer based on the user's question."""
    API_URL = "https://api.openai.com/v1/completions"
 # Replace with the actual API

    API_KEY = os.getenv("OPENAI_API_KEY")


    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": "gpt-4", "prompt": f"Answer this study question: {user_question}", "max_tokens": 200}

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "No response generated.")
    return "Error connecting to AI API."

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome BrainBloom!"})

@app.route("/ask", methods=["POST"])
def ask_question():
    """User submits a study-related question."""
    data = request.json
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "Please provide a study question!"}), 400

    ai_response = get_ai_response(user_question)
    return jsonify({"user_question": user_question, "response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
