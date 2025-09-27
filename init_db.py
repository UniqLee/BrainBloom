import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('database/brainbloom.db')
cursor = conn.cursor()

# This is for loading and executing the schema
with open('schema.sql', 'r') as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()
print(" Schema loaded successfully!")