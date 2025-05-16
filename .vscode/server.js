// Simple Express server to host BrainBloom
const express = require('express');
const path = require('path');
const app = express();
const PORT = 8080;

// Serve static files from the current directory
app.use(express.static(__dirname));

// Ensure all routes serve index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`BrainBloom server running at http://localhost:${PORT}`);
});