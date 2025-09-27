from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai


app = Flask(__name__)





if __name__ == '__main__':
    app.run(debug=True)
