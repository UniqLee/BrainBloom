async function fetchExplanation() {
    // Get the user's input value
    let topic = document.getElementById("topicInput").value;
    let resultDiv = document.getElementById("result");

    if (!topic) {
        alert("Please enter a topic!");
        return;
    }

    // Show a loading message while waiting for the API response
    resultDiv.innerHTML = "<p>⏳ Generating explanation...</p>";

    // Send a POST request to the Flask backend /generate endpoint
    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: topic })
    });

    // Parse the JSON response from the server
    const data = await response.json();
    resultDiv.innerHTML = `<p>${data.explanation}</p>`;

    // Optionally, store the conversation data in Google Sheets
    await fetch("/save_data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic, explanation: data.explanation, quiz_score: "85" })
    });
}