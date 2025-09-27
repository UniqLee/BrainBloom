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




if __name__ == '__main__':
    app.run(debug=True)
