from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_cors import CORS
import sqlite3
from dotenv import load_dotenv
import os
import requests
import time


load_dotenv() 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
CORS(app)


def get_db_connection():
    conn = sqlite3.connect('database/brainbloom.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template('index.html', time=int(time.time()))

def build_prompt(question):
    context=f"""You are personalized ai study assistant called Bloomie, you are meant to provide:  
    Simplified topic explanations, Curated learning resources ,Quick quizzes – Fun and interactive self-testing,
    Think of yourself as a friend who explains tough concepts and ensures people understand.
    Be friendly, helpful, and make learning fun!

    User asked: "{question}"
    Bloomie, respond accordingly.
    """

    return context

@app.route("/bloomie-ai", methods=["GET","POST"])
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
            conn = get_db_connection()
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO topics (title, explanation, subject) VALUES (?, ?, ?)",
                (prompt, feedback, "AI-generated")
            )
            conn.commit()
            conn.close()


        else:
            feedback = "Error getting feedback from AI. Please try again later."

    except Exception as e:
        feedback = f"An error occurred: {str(e)}"


    return render_template("bloomie-ai.html", question=prompt, answer=feedback)


@app.route("/topics")
def view_topics():
    conn = get_db_connection()
    topics = conn.execute("SELECT * FROM topics ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("topics.html", topics=topics)


@app.route("/add-topic", methods=["GET", "POST"])
def add_topic():
    if request.method == "POST":
        title = request.form["title"]
        explanation = request.form["explanation"]
        subject = request.form["subject"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO topics (title, explanation, subject) VALUES (?, ?, ?)",
            (title, explanation, subject)
        )
        conn.commit()
        conn.close()
        flash("Topic added successfully!")
        return redirect(url_for("view_topics"))

    return render_template("add_topic.html")

@app.route("/add-quiz", methods=["GET", "POST"])
def add_quiz():
    conn = get_db_connection()
    topics = conn.execute("SELECT id, title FROM topics").fetchall()

    if request.method == "POST":
        topic_id = request.form["topic_id"]
        question = request.form["question"]
        correct_option = int(request.form["correct_option"])
        options = [request.form[f"option{i}"] for i in range(4)]

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quizzes (topic_id, question, correct_option) VALUES (?, ?, ?)",
            (topic_id, question, correct_option)
        )
        quiz_id = cursor.lastrowid

        for i, option in enumerate(options):
            cursor.execute(
                "INSERT INTO quiz_options (quiz_id, option_text, option_number) VALUES (?, ?, ?)",
                (quiz_id, option, i)
            )

        conn.commit()
        conn.close()
        flash("Quiz added successfully!")
        return redirect(url_for("view_quizzes"))

    return render_template("add_quiz.html", topics=topics)


@app.route("/quizzes")
def view_quizzes():
    conn = get_db_connection()
    quizzes = conn.execute("""
        SELECT quizzes.id, quizzes.question, quizzes.correct_option, topics.title AS topic_title
        FROM quizzes
        JOIN topics ON quizzes.topic_id = topics.id
        ORDER BY quizzes.id DESC
    """).fetchall()
    conn.close()
    return render_template("quizzes.html", quizzes=quizzes)


if __name__ == '__main__':
    app.run(debug=True)
