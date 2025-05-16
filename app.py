from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai


app = Flask(__name__)
CORS(app)

# testing
client = genai.Client(api_key="AIzaSyAP05RYwa__zILpmycarX_UlM_HlA25gYQ")
@app.route("/")
def home_page():
    return render_template("Welcome.html")
    

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Endpoint to generate content using the genai client.
    Expects a JSON payload with a 'prompt' key.
    """
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error":"Missing 'prompt' in request body"}), 400

    prompt = data['prompt']
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return jsonify({"response":response.text}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

#  curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyAP05RYwa__zILpmycarX_UlM_HlA25gYQ" -H 'Content-Type: application/json' -X POST -d '{
#   "contents": [{
#     "parts":[{"text": "Explain how AI works"}]
#     }]
#    }'
