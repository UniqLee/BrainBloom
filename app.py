from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_cors import CORS
import sqlite3
from dotenv import load_dotenv
import os
import requests


load_dotenv() 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


def get_db_connection():
    conn = sqlite3.connect('database/brainbloom.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

def build_prompt(question):
    context=f"""You are personalized ai study assistant called Bloomie, you are meant to provide:  
    Simplified topic explanations, Curated learning resources ,Quick quizzes – Fun and interactive self-testing,
    Think of yourself as a friend who explains tough concepts and ensures people understand.
    Be friendly, helpful, and make learning fun!

    User asked: "{question}"
    Bloomie, respond accordingly.
    """

    return context

@app.route("/bloomie-ai", methods=["POST"])
def talk_to_bloomie():
    prompt = request.form.get("question")
    context = build_prompt(prompt)

    api_url = "https://api.shecodes.io/ai/v1/generate"
    api_key = os.getenv("SHECODES_API_KEY")

    try:
        response = requests.get(api_url, params={
            'prompt': prompt,
            'context': context,
            'key': api_key
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            feedback = data.get("answer", "No feedback received.")
        else:
            feedback = "Error getting feedback from AI. Please try again later."

    except Exception as e:
        feedback = f"An error occurred: {str(e)}"

    # Send the prompt and feedback to the template
    return render_template("bloomie-ai.html", question=prompt, answer=feedback)


if __name__ == '__main__':
    app.run(debug=True)
