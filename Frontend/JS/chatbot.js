document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("userInput");
    const sendMessageButton = document.getElementById("sendMessage");

    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.classList.add("chat-message", sender === "user" ? "user-message" : "bot-message");
        message.textContent = text;
        chatMessages.appendChild(message);
        
        // Auto-scroll to latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function generateBotResponse(userText) {
        const responses = {
            "hello": "Hi there! How can I assist you today?",
            "how are you": "I’m an AI, so I don’t have feelings, but I’m always ready to help!",
            "tell me a joke": "Sure! Why did the student bring a ladder to school? Because they wanted to go to high school!"
        };

        return responses[userText.toLowerCase()] || "I'm not sure how to respond to that. Try asking me something else!";
    }

    sendMessageButton.addEventListener("click", function () {
        const userText = userInput.value.trim();
        if (userText) {
            addMessage(userText, "user");
            setTimeout(() => addMessage(generateBotResponse(userText), "bot"), 500);
        }
        userInput.value = ""; // Clear input after sending
    });
});