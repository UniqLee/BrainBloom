document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    // Function to handle sending messages
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Send message to Python backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Add bot response to chat
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage("Oops! The AI tutor is unavailable at the moment. Try again later.", 'bot');
        });
    }
    
    // Function to add a message to the chat
    function addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'mt-4';
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="card bg-dark text-white shadow-lg p-3 rounded">
                    <p class="fs-5">${message}</p>
                </div>
            `;
        } else {
            // Handle potential HTML content in bot responses
            messageDiv.innerHTML = `
                <div class="card bg-primary text-white shadow-lg p-3 rounded">
                    <p class="fs-5">${message}</p>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        
        // Smooth scrolling to the latest message
        messageDiv.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});