document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("userInput").focus();
});

// Handle 'Enter' key press
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    let chatbox = document.getElementById("chatbox");

    chatbox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;

        if (data.audio) {
            let audio = new Audio("data:audio/mpeg;base64," + data.audio);
            audio.play();
        }
    })
    .catch(error => console.error("Error:", error));
}

// Speech-to-Text Recognition
function startSpeechRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        document.getElementById("userInput").value = transcript;
    };

    recognition.onerror = function(event) {
        alert("Speech recognition error. Please try again.");
    };

    recognition.start();
}

// Handle audio file upload
function uploadAudio() {
    let fileInput = document.getElementById("audioFile");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an audio file.");
        return;
    }

    let formData = new FormData();
    formData.append("audio", file);

    fetch("/upload_audio", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error("Error:", error));
}
