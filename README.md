# Voice Clone Chatbot

A voice-based chatbot that uses AI voice cloning to generate responses in a natural-sounding voice. This project integrates **Flask**, **ElevenLabs API**, and **Gemini API** to enable text and voice interactions.

## 🚀 Features
- **Text-based Chat**: Users can interact with the bot using text input.
- **Voice Cloning**: Generates responses using the cloned voice.
- **Speech-to-Text**: Converts user speech to text for input.
- **Audio Playback**: Bot responds with audio generated using ElevenLabs API.

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: ElevenLabs API (Voice Cloning), Gemini API (Chat Responses)
- **Database**: PostgreSQL (if needed for user data)

## 📂 Folder Structure
```
voice-clone-chatbot/
│── static/
│   ├── css/
│   │   ├── style.css
│   ├── js/
│   │   ├── script.js
│── templates/
│   ├── index.html
│── app.py
│── requirements.txt
│── README.md
```

## 🔧 Installation & Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/barnawalraj001/voice-clone-chatbot.git
   cd voice-clone-chatbot
   ```

2. **Create a virtual environment** (Optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   - Get an **ElevenLabs API Key** from [ElevenLabs](https://elevenlabs.io)
   - Get a **Gemini API Key** from [Google AI](https://ai.google.dev)
   - Add them to a `.env` file:
     ```
     ELEVENLABS_API_KEY=your-elevenlabs-key
     GEMINI_API_KEY=your-gemini-key
     ```

5. **Run the Flask server**
   ```sh
   python app.py
   ```
   The app will be available at: **`http://127.0.0.1:5000/`**

## 🎤 How to Use
1. **Text Chat**: Enter a message in the chatbox and get a response.
2. **Voice Input**: Click the microphone button to use speech-to-text.
3. **Voice Output**: Listen to the chatbot's response in a cloned voice.

## 📌 Future Enhancements
- 🌟 **User Authentication** (Login/Signup)
- 🎭 **Multiple Voice Profiles**
- 🔄 **Integration with More AI Models**

## 📝 License
This project is licensed under the **MIT License**.

---

💡 **Contributions Welcome!** If you'd like to improve this project, feel free to open a Pull Request. 😃
