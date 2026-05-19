/* =========================
   CHAT SYSTEM (FOCUSFLOW AI)
========================= */

function typeText(element, text, speed = 12) {
    let i = 0;
    element.innerHTML = "";

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    if (!input || !chatBox) {
        console.error("Chat elements not found");
        return;
    }

    const message = input.value.trim();
    if (!message) return;

    /* USER MESSAGE */
    const userMsg = document.createElement("div");
    userMsg.className = "msg user";
    userMsg.innerText = message;
    chatBox.appendChild(userMsg);

    input.value = "";

    /* AI PLACEHOLDER */
    const aiMsg = document.createElement("div");
    aiMsg.className = "msg ai";
    aiMsg.innerText = "Thinking...";
    chatBox.appendChild(aiMsg);

    chatBox.scrollTop = chatBox.scrollHeight;

    /* CALL BACKEND */
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        typeText(aiMsg, data.response, 10);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => {
        aiMsg.innerText = "Error: AI not responding";
        console.error(err);
    });
}

/* =========================
   ENTER KEY SUPPORT
========================= */

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("userInput");

    if (!input) return;

    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});

/* =========================
   DEBUG HELP
========================= */

console.log("FocusFlow AI script loaded successfully 🚀");