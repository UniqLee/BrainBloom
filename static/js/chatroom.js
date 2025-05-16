document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const communityInput = document.getElementById("communityInput");
    const sendCommunityMessageButton = document.getElementById("sendCommunityMessage");

    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.classList.add("chat-message", sender === "user" ? "user-message" : "community-message");
        message.textContent = text;
        chatMessages.appendChild(message);
        
        // Auto-scroll to latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendCommunityMessageButton.addEventListener("click", function () {
        const userText = communityInput.value.trim();
        if (userText) {
            addMessage(userText, "user");
            setTimeout(() => addMessage("Someone from the community responded!", "community"), 1000);
        }
        communityInput.value = ""; // Clear input after sending
    });
});