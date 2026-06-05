/* =========================
   TYPE EFFECT
========================= */

function typeEffect(element, html, speed = 5) {

    element.innerHTML = html;

    if (window.MathJax) {

        MathJax.typesetPromise([element]);

    }
}


/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {

    const input = document.getElementById("message");

    const msg = input.value.trim();

    if (!msg) return;

    const chatBox = document.getElementById("chat-box");

    /* =========================
       USER MESSAGE
    ========================= */

    const userDiv = document.createElement("div");

    userDiv.className = "message user-message";

    userDiv.innerHTML = msg;

    chatBox.appendChild(userDiv);

    /* CLEAR INPUT */

    input.value = "";

    /* AUTO SCROLL */

    chatBox.scrollTop = chatBox.scrollHeight;

    /* =========================
       LOADER
    ========================= */

    const loader = document.createElement("div");

    loader.className = "loader";

    loader.innerHTML = "🧠 AI is analyzing...";

    chatBox.appendChild(loader);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: msg
            })

        });

        const data = await response.json();

        /* REMOVE LOADER */

        loader.remove();

        /* =========================
           AI MESSAGE
        ========================= */

        const aiDiv = document.createElement("div");

        aiDiv.className = "message ai-message";

        chatBox.appendChild(aiDiv);

        /* MARKDOWN FORMAT */

        const formatted = marked.parse(data.response);

        /* TYPE EFFECT */

        typeEffect(aiDiv, formatted);

        /* AUTO SCROLL */

        chatBox.scrollTop = chatBox.scrollHeight;

    }

    catch (error) {

        loader.remove();

        const errorDiv = document.createElement("div");

        errorDiv.className = "message ai-message";

        errorDiv.innerHTML =
            "⚠ AI temporarily unavailable.";

        chatBox.appendChild(errorDiv);
    }
}


/* =========================
   ENTER KEY SEND
========================= */

document
.getElementById("message")
.addEventListener("keydown", function(e) {

    if (e.key === "Enter") {

        e.preventDefault();

        sendMessage();
    }
});