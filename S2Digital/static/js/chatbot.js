// simple chat + contact submit handlers
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contactForm");
  const emailRe = /^[^@]+@[^@]+\.[^@]+$/;
  const mobileRe = /^[+\d().\-\s]{7,40}$/;

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());

      // client-side validation
      if (!data.name || !data.email || !data.message) {
        showContactResult("Please fill all fields.", false);
        return;
      }
      if (data.name.length > 120) {
        showContactResult("Name is too long.", false);
        return;
      }
      if (data.email.length > 200 || !emailRe.test(data.email)) {
        showContactResult("Invalid email.", false);
        return;
      }
      if (data.message.length > 2000) {
        showContactResult("Message is too long.", false);
        return;
      }
      if (/[<>]/.test(data.name) || /[<>]/.test(data.message)) {
        showContactResult("Please remove angle brackets from input.", false);
        return;
      }
      // optional mobile validation
      if (data.mobile) {
        if (data.mobile.length > 40 || !mobileRe.test(data.mobile) || /[<>]/.test(data.mobile)) {
          showContactResult("Invalid mobile number.", false);
          return;
        }
      }

      let res;
      try {
        res = await fetch("/contact/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
      } catch (err) {
        showContactResult("Network error. Please try again.", false);
        return;
      }

      // Robust response parsing
      let json;
      const ct = res.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        try {
          json = await res.json();
        } catch (err) {
          json = { ok: false, error: "Invalid JSON response from server" };
        }
      } else {
        const txt = await res.text();
        try {
          json = JSON.parse(txt);
        } catch (err) {
          json = { ok: false, error: "Invalid response: " + txt };
        }
      }

      if (json.ok) {
        showContactResult("Message sent. Thank you!", true);
        // Clear the form fields
        try { form.reset(); } catch (e) {}
        // clear the status message after 5 seconds
        setTimeout(() => {
          const out = document.getElementById("contactResult");
          if (out) out.textContent = "";
        }, 5000);
      } else {
        showContactResult(json.error || "Error sending message.", false);
      }
    });
  }

  function showContactResult(txt, ok) {
    const out = document.getElementById("contactResult");
    if (!out) return;
    out.textContent = txt;
    out.style.color = ok ? "green" : "red";
  }

  const chatSend = document.getElementById("chatSend");
  const chatInput = document.getElementById("chatInput");
  const chatLog = document.getElementById("chatLog");
  if (chatSend && chatInput && chatLog) {
    chatSend.addEventListener("click", async () => {
      const text = chatInput.value.trim();
      if (!text) return;
      appendLine("You: " + text);
      chatInput.value = "";
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const json = await res.json();
      appendLine("Bot: " + (json.reply || json.error || "No reply"));
    });
  }

  function appendLine(s) {
    const p = document.createElement("div");
    p.textContent = s;
    chatLog.appendChild(p);
    chatLog.scrollTop = chatLog.scrollHeight;
  }
});