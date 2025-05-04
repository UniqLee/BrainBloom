from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google.generativeai as genai
import logging

# 🔹 Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# 🔹 Configure logging for debugging
logging.basicConfig(level=logging.INFO)

# 🔹 Authenticate with Google Sheets API
def authenticate_google_sheets():
    """Authenticates and returns the Google Sheets client."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
        client = gspread.authorize(creds)
        logging.info("✅ Google Sheets authentication successful")
        return client
    except Exception as e:
        logging.error(f"❌ Google Sheets authentication failed: {e}")
        return None

# 🔹 Initialize Google Sheets Client
client = authenticate_google_sheets()

# 🔹 Function to safely access Google Sheets worksheet
def get_worksheet(sheet_name):
    """Returns worksheet if available, otherwise logs an error."""
    if client:
        try:
            return client.open_by_key("18f2cExe8U53cBg16XOI9O4lVH9CucIcEAc_1RPulppU").worksheet(sheet_name)
        except Exception as e:
            logging.error(f"❌ Failed to access worksheet '{sheet_name}': {e}")
            return None
    return None

# 🔹 Configure Google Gemini AI API
try:
    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    logging.info("✅ Google Gemini AI API initialized successfully")
except Exception as e:
    logging.error(f"❌ Failed to initialize Gemini AI API: {e}")

# 🔹 Home Route
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Additional Frontend Routes (Registering Dedicated Pages)
@app.route("/chatbot")
def chatbot():
    return render_template("Chatbot/chatbot.html")

@app.route("/educational")
def educational():
    return render_template("Educational level/educational.html")

@app.route("/login")
def login():
    return render_template("Login page/login.html")

@app.route("/features")
def features():
    return render_template("Main Feature/features.html")

@app.route("/promotional")
def promotional():
    return render_template("Promotional Page/promotional.html")

@app.route("/signup")
def signup():
    return render_template("SignUp page/signup.html")

@app.route("/welcome")
def welcome():
    return render_template("Welcome page/welcome.html")

# 🔹 AI Content Generation Route
@app.route('/generate', methods=['POST'])
def generate_content():
    """Calls Gemini API to generate study explanations."""
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "❌ Missing 'prompt' in request"}), 400

        response = genai.generate_text(prompt=prompt, model="gemini-2.0-pro")
        return jsonify({"explanation": response.result})
    except Exception as e:
        logging.error(f"❌ Error generating content: {e}")
        return jsonify({"error": "Failed to generate content"}), 500

# 🔹 Save Data to Google Sheets Route
@app.route('/save_data', methods=['POST'])
def save_data():
    """Saves study topics, AI-generated explanations, and quiz scores to Google Sheets."""
    try:
        data = request.get_json()
        sheet = get_worksheet("BrainBloom_Data")

        if not sheet:
            return jsonify({"error": "❌ Google Sheets integration not available"}), 500

        sheet.append_row([data.get("topic", ""), data.get("explanation", ""), data.get("quiz_score", "")])
        return jsonify({"message": "✅ Data saved successfully!"})
    except Exception as e:
        logging.error(f"❌ Error saving data to Google Sheets: {e}")
        return jsonify({"error": "Failed to save data"}), 500

# 🔹 Retrieve Study Data Route
@app.route('/get_data', methods=['GET'])
def get_data():
    """Retrieves stored study data from Google Sheets."""
    try:
        sheet = get_worksheet("BrainBloom_Data")

        if not sheet:
            return jsonify({"error": "❌ Google Sheets integration not available"}), 500

        records = sheet.get_all_records()
        return jsonify({"data": records})
    except Exception as e:
        logging.error(f"❌ Error retrieving data: {e}")
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)

#  curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyAP05RYwa__zILpmycarX_UlM_HlA25gYQ" -H 'Content-Type: application/json' -X POST -d '{
#   "contents": [{
#     "parts":[{"text": "Explain how AI works"}]
#     }]
#    }'
