from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv() 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

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
