import sqlite3

# Database connection
def connect_db():
    return sqlite3.connect("data/quizapp.db")

# User login
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns None if not found

# User registration
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():  # If user already exists
        conn.close()
        return False
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True

def fetch_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories


# Fetch quiz questions based on category
def fetch_questions(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE category_id=?", (category_id,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Update user score in the database
def update_score(user_id, score, category_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (user_id, score, category_id) VALUES (?, ?, ?)", (user_id, score, category_id))
    conn.commit()
    conn.close()

# Create the database and tables if they do not exist
def create_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')

    # Create categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )''')

    # Create questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        options TEXT NOT NULL,  -- Store options as a JSON string
        correct_option INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')

    # Create scores table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')

    # Prepopulate categories and questions
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Mathematics'), ('Science'), ('Technology'), ('Automobiles'), ('Games')")
    conn.commit()
    conn.close()

# Call create_db() to initialize the database
create_db()
