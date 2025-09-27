from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
<<<<<<< HEAD
from google import genai
import sqlite3


=======
from dotenv import load_dotenv
import os
>>>>>>> f80d8e6e5fea0e47985c08fff7441005805ad670


load_dotenv() 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

<<<<<<< HEAD

def get_db_connection():
    conn = sqlite3.connect('database/brainbloom.db')
    conn.row_factory = sqlite3.Row
    return conn
# testing
client = genai.Client(api_key="AIzaSyAP05RYwa__zILpmycarX_UlM_HlA25gYQ")
=======
>>>>>>> f80d8e6e5fea0e47985c08fff7441005805ad670
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/bloomie-ai")
def talk_to_bloomie():
    return render_template("bloomie-ai.html")

def build_prompt():
    context="""You are personalized ai study assistant called Bloomie, you are meant to provide:  
    Simplified topic explanations, Curated learning resources ,Quick quizzes – Fun and interactive self-testing,
    Think of yourself as a friend who explains tough concepts and ensures people understand."""
    
    return context



if __name__ == '__main__':
    app.run(debug=True)
