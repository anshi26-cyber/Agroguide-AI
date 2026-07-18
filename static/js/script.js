// =========================
// THEME
// =========================

window.toggleTheme = function () {
    const html = document.documentElement;
    const btn = document.getElementById("theme-btn");

    html.classList.toggle("dark");

    if (html.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        if (btn) btn.innerHTML = "☀️";
    } else {
        localStorage.setItem("theme", "light");
        if (btn) btn.innerHTML = "🌙";
    }
};

window.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("theme-btn");

    if (localStorage.getItem("theme") === "dark") {
        document.documentElement.classList.add("dark");
        if (btn) btn.innerHTML = "☀️";
    } else {
        document.documentElement.classList.remove("dark");
        if (btn) btn.innerHTML = "🌙";
    }

    // Chat Button
    const chatToggle = document.getElementById("chat-toggle");

    if (chatToggle) {
        chatToggle.addEventListener("click", toggleChat);
    }

    // Enter Key
    const input = document.getElementById("message");

    if (input) {
        input.addEventListener("keypress", function (e) {

            if (e.key === "Enter") {
                e.preventDefault();
                sendTypedMessage();
            }

        });
    }

});


// =========================
// CHAT WINDOW
// =========================

let recognition = null;

function toggleChat() {

    const chat = document.getElementById("chat-window");

    if (chat) {
        chat.classList.toggle("hidden");
    }

}


// =========================
// ADD MESSAGE
// =========================

function addMessage(user, text) {

    const box = document.getElementById("chat-box");

    if (!box) return;

    const isBot = user === "🤖";

    box.innerHTML += `
        <div class="flex ${isBot ? "justify-start" : "justify-end"}">

            <div class="${isBot ? "bg-green-700" : "bg-slate-700"} px-4 py-3 rounded-2xl max-w-[80%]">

                <b>${user}</b><br>

                ${text}

            </div>

        </div>
    `;

    box.scrollTop = box.scrollHeight;

}


// =========================
// SEND TEXT MESSAGE
// =========================

function sendTypedMessage() {

    const input = document.getElementById("message");

    if (!input) return;

    const text = input.value.trim();

    if (!text) return;

    addMessage("🧑", text);

    input.value = "";

    sendMessage(text);

}


// =========================
// VOICE INPUT
// =========================

function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert("Speech Recognition is not supported in this browser.");

        return;
    }

    recognition = new SpeechRecognition();

    recognition.lang = "en-IN";

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;

    recognition.onresult = function (event) {

        const text = event.results[0][0].transcript;

        addMessage("🧑", text);

        sendMessage(text);

    };

    recognition.onerror = function () {

        alert("Voice recognition failed.");

    };

    recognition.start();

}


// =========================
// SPEAK RESPONSE
// =========================

function speak(text) {

    if (!("speechSynthesis" in window)) return;

    speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);

    utter.lang = "en-IN";

    speechSynthesis.speak(utter);

}


// =========================
// CSRF TOKEN
// =========================

function getCSRFToken() {

    const meta = document.querySelector('meta[name="csrf-token"]');

    return meta ? meta.content : "";

}


// =========================
// SEND TO DJANGO
// =========================

function sendMessage(text) {

    fetch("/chatbot/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "X-CSRFToken": getCSRFToken()

        },

        body: JSON.stringify({

            message: text,

            lang: "en"

        })

    })

    .then(response => {

        if (!response.ok) {

            throw new Error("Network Error");

        }

        return response.json();

    })

    .then(data => {

        addMessage("🤖", data.reply);

        speak(data.reply);

    })

    .catch(error => {

        console.error(error);

        addMessage("🤖", "⚠️ Something went wrong.");

    });

}