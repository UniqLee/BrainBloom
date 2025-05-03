from flask import Flask, request, jsonify
from google import genai


app = Flask(__name__)


client = genai.Client(api_key="AIzaSyAP05RYwa__zILpmycarX_UlM_HlA25gYQ")

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Endpoint to generate content using the genai client.
    Expects a JSON payload with a 'prompt' key.
    """
    data = request.get_json()
    if not data or 'prompt' not in data:
        return "Missing 'prompt' in request body", 400

    prompt = data['prompt']
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text, 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)