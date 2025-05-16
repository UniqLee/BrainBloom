document.addEventListener("DOMContentLoaded", function() {
    const sendMessageButton = document.getElementById("sendMessage");
    const userInputField = document.getElementById("userInput");
    const chatMessages = document.getElementById("chat-messages");
  
    function appendMessage(content, sender) {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add(sender);
      messageDiv.textContent = content;
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;  // Scroll to the latest message
    }
  
    sendMessageButton.addEventListener("click", function() {
      const userMessage = userInputField.value.trim();
      if (userMessage === "") {
        return; // Don't send an empty message
      }
  
      appendMessage("You: " + userMessage, "user-message");
  
      // Clear the input field
      userInputField.value = "";
  
      // Send the user input to the Flask backend (ensure the URL is correct)
      fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: userMessage }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.response) {
          appendMessage("Bot: " + data.response, "bot-message");
        } else {
          appendMessage("Bot: Sorry, I couldn't understand that.", "bot-message");
        }
      })
      .catch(error => {
        console.error("Error:", error);
        appendMessage("Bot: An error occurred. Please try again.", "bot-message");
      });
    });
  });
  