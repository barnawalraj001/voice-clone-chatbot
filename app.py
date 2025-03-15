import os
import google.generativeai as genai
import base64
import requests
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure API Keys
GEMINI_API_KEY = "AIzaSyBLoVssOFRozRvSjEOXfhWhOScICdMZbWE"
ELEVENLABS_API_KEY = "sk_7511c84227d802367c88c839114b882a7a5c62d1132d6835"
# Configure APIs
genai.configure(api_key=GEMINI_API_KEY)

# Default Voice ID (Will change if user clones voice)
DEFAULT_VOICE_ID = "CwhRBWXzGAHq8TQ4Fs17"

# Folder Configurations
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a"}

# In-memory storage for cloned voices (use DB in production)
user_voice_ids = {}

def allowed_file(filename):
    """Check if uploaded file has a valid format."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_gemini_response(user_input):
    """Fetch text response from Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        prompt = """
        You are a banking specialist, knowledgeable in savings, fixed deposits, loans, interest rates, investment options, and digital banking. 
        Provide clear, accurate, and well-explained responses based on general banking principles, without real-time data access.
        Be professional and concise and never use bold letters.
        """

        full_input = f"{prompt}\n\nUser: {user_input}\nAssistant:"
        response = model.generate_content(full_input)

        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def generate_speech(text, user_id=None):
    """Generate speech using ElevenLabs cloned voice."""
    voice_id = user_voice_ids.get(user_id, DEFAULT_VOICE_ID)  # Use cloned voice if available

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
    else:
        print("TTS Error:", response.json())
        return None


def clone_voice(file_path, user_id):
    """Upload a voice sample to ElevenLabs and get a new voice ID."""
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    files = {"files": open(file_path, "rb")}
    data = {"name": f"User_{user_id}", "labels": "{}"}

    response = requests.post(url, headers=headers, files=files, data=data)

    print("Response Code:", response.status_code)  # Print status code
    print("Response JSON:", response.json())  # Print full response

    if response.status_code == 200:
        voice_id = response.json()["voice_id"]
        user_voice_ids[user_id] = voice_id  # Store voice ID for future use
        return voice_id
    else:
        print("Voice Cloning Error:", response.json())  # Print exact error
        return None



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle user messages and return both text and voice responses."""
    data = request.json
    user_message = data.get("message", "")
    user_id = data.get("user_id", "default")

    bot_response = get_gemini_response(user_message)
    audio_data = generate_speech(bot_response, user_id)

    if audio_data:
        return jsonify({"response": bot_response, "audio": audio_data})
    else:
        return jsonify({"response": bot_response, "error": "Speech synthesis failed"})


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    """Handle audio file upload, save it, and send it for voice cloning."""
    user_id = request.form.get("user_id", "default")

    if "audio" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["audio"]
    
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"message": "Invalid file format"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Clone voice and get new voice_id
    voice_id = clone_voice(file_path, user_id)

    if voice_id:
        return jsonify({"message": "Voice cloned successfully!", "voice_id": voice_id})
    else:
        return jsonify({"message": "Voice cloning failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
