// index.js
// CS3100 Encryption Project - Frontend
// Author: Vip Monty (Group 2)
// Description: Sends plaintext messages to the FastAPI backend for encryption,
// and retrieves decrypted messages by name.

document.addEventListener("DOMContentLoaded", () => {
    const sendForm = document.getElementById("message-form");
    const getForm = document.getElementById("get-message-form");
    const display = document.querySelector(".message-display");

    // -----------------------------
    // Send (Encrypt + Store)
    // -----------------------------
    sendForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const message = document.getElementById("message").value.trim();

        if (!name || !message) {
            display.innerHTML = `<p style="color:red;">Please enter both a name and a message.</p>`;
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, message }),
            });

            if (!response.ok) throw new Error("Failed to send message");

            const data = await response.json();
            display.innerHTML = `
                <h3>✅ Message Encrypted & Stored</h3>
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Encrypted Message:</strong> ${data.encrypted_message}</p>
                <p><strong>Key:</strong> ${data.key}</p>
                <p style="color:gray;">(Stored securely in the backend database)</p>
            `;
        } catch (err) {
            console.error(err);
            display.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
        }
    });

    // -----------------------------
    // Retrieve (Decrypt)
    // -----------------------------
    getForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("getName").value.trim();
        if (!name) {
            display.innerHTML = `<p style="color:red;">Please enter a name to retrieve.</p>`;
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/message/${name}`);
            if (!response.ok) {
                if (response.status === 404) {
                    display.innerHTML = `<p style="color:red;">No message found for "${name}".</p>`;
                    return;
                }
                throw new Error("Failed to fetch message");
            }

            const data = await response.json();
            display.innerHTML = `
                <h3>🔓 Message Decrypted</h3>
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Decrypted Message:</strong> ${data.message}</p>
            `;
        } catch (err) {
            console.error(err);
            display.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
        }
    });
});
