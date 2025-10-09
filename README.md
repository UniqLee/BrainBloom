# 🌱 BrainBloom – Your AI-Powered Study Assistant

BrainBloom is an intelligent, AI-driven study assistant web application built to empower learners by promoting critical thinking, self-paced learning, and meaningful collaboration.

---

## 💡 What Is BrainBloom?

**BrainBloom** is a personalized AI learning platform that helps users deepen their understanding of subjects through conversational interactions with **Bloomie** — your friendly AI assistant.

> Instead of providing direct answers, Bloomie encourages users to explore concepts and discover solutions on their own — making learning active, engaging, and thought-provoking.

In addition to AI guidance, BrainBloom includes a **peer-to-peer chatroom** where learners can ask questions, share insights, and collaborate in real-time.

---

## ✨ Features

- 👤 **User Authentication** – Sign up, log in securely with hashed passwords.
- 🤖 **AI Study Assistant** – Ask Bloomie questions and get intelligent, context-aware responses.
- 🎯 **Goal-Oriented Learning** – Define your education level, learning goals, and subjects for a personalized experience.
- 📚 **Topic & Quiz Management** – Add learning topics, explanations, and create quizzes to test your knowledge.
- 💬 **Peer Chatroom** – Join real-time discussions with fellow students to ask or answer questions.
- 🔒 **Secure Backend** – Passwords are securely hashed; user data is protected using SQLite and Flask best practices.

---

## 🔧 Tech Stack

| Layer        | Technology                      |
|--------------|----------------------------------|
| Backend      | Python, Flask, SQLite            |
| Frontend     | HTML5, CSS3, JavaScript          |
| Styling      | CSS Variables, Flexbox, Custom UI|
| AI           | External API via SheCodes        |
| Security     | `werkzeug.security`, Flask `session` |
| API Handling | `requests`, `dotenv`             |

---

## 👨‍💻 Developer Team

| Name               | Role                 | Contributions                                                                 |
|--------------------|----------------------|------------------------------------------------------------------------------|
| **[Amohelang Mohlomi]**     | Backend Developer    | AI integration, database management (SQLite), secure user authentication, Flask routing |
| **[Ayanda Khumalo]**    | Frontend Developer   | Designed and styled the UI, implemented responsive forms and layouts         |
| **[Lerato Mosia]**   | Fullstack Developer  | Integrated the database, helped connect frontend with backend logic, debugging   |

---

## 📁 Project Structure

brainbloom/
├── static/
│ └── css/
│ └── auth.css
├── templates/
│ ├── signup.html
│ ├── login.html
│ ├── bloomie-ai.html
│ ├── quizzes.html
│ ├── add_quiz.html
│ └── other templates...
├── database/
│ └── brainbloom.db
├── app.py
├── requirements.txt
├── .env
└── README.md

yaml
Copy code

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/brainbloom.git
cd brainbloom
```
### 2. Create and Activate a Virtual Environment
Copy code
``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
Copy code
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a .env file in the root directory and add your API key:
Copy code
```bash
SHECODES_API_KEY=your_api_key_here
```
### 5. Run the Application
Copy code
```bash
python app.py
Visit your app at: http://localhost:5000
```

🗃️ Database Schema Overview
The app uses SQLite and includes the following tables:

users – Stores user information (email, password hash, education level, etc.)

topics – Stores AI-generated and user-created learning topics

resources – Stores additional learning resources linked to topics

quizzes – Stores questions and correct answers

quiz_options – Stores options for multiple-choice questions

📦 Requirements
Install all dependencies with:

bash
Copy code
pip install -r requirements.txt
Typical packages used:

Flask

Flask-Cors

Werkzeug

requests

python-dotenv

🌐 Live Features Overview
Signup Form:
Collects user’s first name, last name, email, password, education level, subjects of interest, and learning goals.

AI Assistant (Bloomie):
Powered by an API that responds contextually to user queries without giving away direct answers.

Flash Messages:
Visual feedback on signup, login, and errors using Flask’s flash() and custom CSS styles.

Chatroom (WIP or Implemented):
Peer-to-peer communication for deeper collaboration.

🛡 Security Notes
Passwords are never stored as plain text; they are hashed using Werkzeug’s generate_password_hash().

User sessions are handled securely with Flask session management.

Inputs are sanitized via HTML forms and server-side validation.

📬 Contact & Contributions
If you want to contribute, report issues, or collaborate, feel free to:

Submit a pull request

Open an issue

Contact us via GitHub

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgements
Thanks to SheCodes AI API for enabling smart learning with Bloomie.

Inspired by educators and learners who believe in making learning more accessible, engaging, and interactive.




