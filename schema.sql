CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    education_level TEXT NOT NULL,
    subjects TEXT NOT NULL,
    goal TEXT NOT NULL
);

-- Topics table
CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    explanation TEXT NOT NULL,
    subject TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Resources table
CREATE TABLE resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    type TEXT CHECK(type IN ('video', 'article', 'other')),
    FOREIGN KEY(topic_id) REFERENCES topics(id)
);

-- Quizzes table
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    question TEXT NOT NULL,
    correct_option INTEGER,
    FOREIGN KEY(topic_id) REFERENCES topics(id)
);

-- Quiz options table
CREATE TABLE quiz_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    option_text TEXT NOT NULL,
    option_number INTEGER CHECK(option_number BETWEEN 0 AND 3),
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
);

