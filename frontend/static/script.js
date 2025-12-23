async function sendQuestion() {
  const qBox = document.getElementById("q");
  const question = qBox.value.trim();
  if (!question) return;
  appendMessage("You", question, "you");
  qBox.value = "";

  appendMessage("Bot", "Thinking...", "bot", true);

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question})
    });
    const data = await res.json();
    // remove the 'Thinking...' last bot message
    removeThinking();
    if (data.error) {
      appendMessage("Bot", "Error: " + data.error, "bot");
      return;
    }
    // answer text
    appendMessage("Bot", data.answer, "bot");

    // citations
    if (data.citations && data.citations.length) {
      const html = data.citations.map(c => {
        return `<a class="cite-link" href="${c.link}" target="_blank">${c.text}</a>`;
      }).join(" · ");
      appendCitation(html);
    }
  } catch (e) {
    removeThinking();
    appendMessage("Bot", "Request failed: " + e.toString(), "bot");
  }
}

function appendMessage(who, text, cls, thinking=false) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.innerHTML = `<strong>${who}:</strong> <div>${escapeHtml(text).replace(/\n/g, "<br/>")}</div>`;
  if (thinking) div.id = "thinking";
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function removeThinking() {
  const t = document.getElementById("thinking");
  if (t) t.remove();
}

function appendCitation(html) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "citation";
  div.innerHTML = `<strong>References:</strong> ${html}`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function escapeHtml(unsafe) {
  return unsafe
       .replace(/&/g, "&amp;")
       .replace(/</g, "&lt;")
       .replace(/>/g, "&gt;")
       .replace(/"/g, "&quot;")
       .replace(/'/g, "&#039;");
}

document.getElementById("send").addEventListener("click", sendQuestion);
document.getElementById("q").addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendQuestion();
});
