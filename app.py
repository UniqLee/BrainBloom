import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_cors import CORS
import sqlite3
from dotenv import load_dotenv
import os
import requests
import time
from werkzeug.security import generate_password_hash,check_password_hash
from flask_socketio import SocketIO, emit





load_dotenv() 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
CORS(app)

socketio = SocketIO(app,async_mode='eventlet')

def get_db_connection():
    conn = sqlite3.connect('database/brainbloom.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template('index.html', time=int(time.time()))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        education = request.form.get('education')
        subject = request.form.get('subjects')
        goal = request.form.get('goal')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('signup.html')


        hashed_password = generate_password_hash(password)

        success = add_user(email,hashed_password, first_name,last_name, education, subject, goal)

        if success:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already exists. Please use a different one.', 'error')

    return render_template('signup.html')

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password= request.form.get("password")
        user = get_user(email)
        if user and check_password_hash(user['user_password'], password):  
            session['email'] = email  
            flash('Logged in successfully!', 'success')
            return redirect(url_for('chatroom'))
        else:
            flash("User does not exist!")

    return render_template("login.html")

def build_prompt(question):
    context=f"""You are personalized ai study assistant called Bloomie, you are meant to provide:  
    Simplified topic explanations, Curated learning resources ,Quick quizzes – Fun and interactive self-testing,
    Think of yourself as a friend who explains tough concepts and ensures people understand.
    Be friendly, helpful, and make learning fun!

    User asked: "{question}"
    Bloomie, respond accordingly.
    """

    return context

@app.route("/bloomie-ai", methods=["GET", "POST"])
def talk_to_bloomie():
    chat_history = session.get("chat_history", [])

    if not chat_history:
        chat_history.append({
            "role": "bloomie",
            "text": "Hi there! 🌱 I'm Bloomie, your study buddy. Ask me anything about your topic!"
        })
        session["chat_history"] = chat_history

    if request.method == "POST":
        prompt = request.form.get("question")
        context = build_prompt(prompt)
        print(f"Context: {context}")
        print(f"Prompt: {prompt}")
        api_url = "https://api.shecodes.io/ai/v1/generate"
        api_key = os.getenv("SHECODES_API_KEY")

        try:
            response = requests.get(api_url, params={
                'prompt': prompt,
                'context': context,
                'key': api_key
            }, timeout=30)
            print("Inside try")
            if response.status_code == 200:
                data = response.json()
                feedback = data.get("answer", "No feedback received.")

                conn = get_db_connection()
                conn.execute(
                    "INSERT INTO topics (title, explanation, subject) VALUES (?, ?, ?)",
                    (prompt, feedback, "AI-generated")
                )
                conn.commit()
                conn.close()

                chat_history.append({"role": "user", "text": prompt})
                chat_history.append({"role": "bloomie", "text": feedback})
                session["chat_history"] = chat_history

            else:
                feedback = "Error getting feedback from Bloomie. Please try again later."
                chat_history.append({"role": "bloomie", "text": feedback})

        except Exception as e:
            feedback = f"An error occurred: {str(e)}"
            chat_history.append({"role": "bloomie", "text": feedback})

        return render_template("bloomie-ai.html", chat_history=chat_history)

    return render_template("bloomie-ai.html", chat_history=chat_history)


@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    session.pop("chat_history", None)
    return redirect(url_for("talk_to_bloomie"))


@app.route("/topics")
def view_topics():
    user_id = get_user(session['email'])['id']
    conn = get_db_connection()
    topics = conn.execute("SELECT * FROM topics WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return render_template("topics.html", topics=topics)

@app.route("/add-topic", methods=["GET", "POST"])
def add_topic():
    if request.method == "POST":
        title = request.form["title"]
        explanation = request.form["explanation"]
        subject = request.form["subject"]
        user = get_user(session['email'])
        user_id = user['id']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO topics (user_id, title, explanation, subject) VALUES (?, ?, ?, ?)",
            (user_id, title, explanation, subject)
        )
        conn.commit()
        conn.close()
        flash("Topic added successfully!")
        return redirect(url_for("view_topics"))

    return render_template("add_topic.html")

@app.route("/add-quiz", methods=["GET", "POST"])
def add_quiz():
    conn = get_db_connection()
    topics = conn.execute("SELECT id, title FROM topics WHERE user_id = ?", (get_user(session['email'])['id'],)).fetchall()

    if request.method == "POST":
        topic_id = request.form["topic_id"]
        question = request.form["question"]
        correct_option_raw = request.form["correct_option"]
        user_id = get_user(session['email'])['id']

        if not correct_option_raw.isdigit():
            flash("Please select a valid correct option.", "error")
            return render_template("add_quiz.html", topics=topics)

        correct_option = int(correct_option_raw)
        options = [request.form[f"option{i}"] for i in range(4)]

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quizzes (user_id, topic_id, question, correct_option) VALUES (?, ?, ?, ?)",
            (user_id, topic_id, question, correct_option)
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
def quizzes():
    user_id = get_user(session['email'])['id']
    conn = get_db_connection()
    quizzes = conn.execute("""
        SELECT quizzes.id, quizzes.question, quizzes.correct_option, topics.title AS topic_title
        FROM quizzes
        JOIN topics ON quizzes.topic_id = topics.id
        WHERE quizzes.user_id = ?
        ORDER BY quizzes.id DESC
    """, (user_id,)).fetchall()
    conn.close()
    return render_template("quizzes.html", quizzes=quizzes)

def add_user(email, password_hash, first_name, last_name, education, subject, goal):
    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO users (email, user_password, first_name, last_name, education_level, subjects, goal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (email, password_hash, first_name, last_name, education, subject, goal))
        conn.commit()
        conn.close()
        print("User added successfully!")  # ✅ DEBUG LOG
        return True
    except sqlite3.IntegrityError:
        print("IntegrityError: Email already exists!")  # ✅ DEBUG LOG
        return False
    except Exception as e:
        print(f"Exception in add_user: {e}")  # ✅ DEBUG LOG
        return False


def get_user(user_email):
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM users WHERE email = ?', (user_email,))
    return cursor.fetchone()

@app.route("/chatroom")
def chatroom():
    if 'email' not in session:
        flash("Please log in to access the chatroom.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    messages = conn.execute("SELECT sender, message, timestamp FROM chatroom_messages ORDER BY timestamp ASC").fetchall()
    conn.close()

    return render_template("chatroom.html", email=session['email'], messages=messages)

@socketio.on('send_message')
def handle_message(data):
    sender = data['sender']
    message = data['message']

    # Save to database
    conn = get_db_connection()
    conn.execute("INSERT INTO chatroom_messages (sender, message) VALUES (?, ?)", (sender, message))
    conn.commit()
    conn.close()

    # Broadcast message to all clients
    emit('receive_message', {
        'sender': sender,
        'message': message
    }, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
