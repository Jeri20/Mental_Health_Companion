import sqlite3

# Create a connection to your SQLite database
conn = sqlite3.connect("mindmate.db", check_same_thread=False)
c = conn.cursor()

# Initialize all tables including users
def init_db():
    # User login table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''CREATE TABLE IF NOT EXISTS questionnaire (
                    user_id TEXT, gad_score INTEGER, phq_score INTEGER, date TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS journal (
                    user_id TEXT, entry TEXT, sentiment REAL, date TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS mood (
                    user_id TEXT, date TEXT, mood_score INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS chat (
                    user_id TEXT, message TEXT, sentiment REAL, date TEXT)''')

    conn.commit()

# User Registration
def register_user(email, password):
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists

# User Login
def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()  # returns (id, email, password)

# Store GAD/PHQ Scores
def store_questionnaire(user_id, gad_score, phq_score, date):
    c.execute('''
    INSERT INTO questionnaire (user_id, gad_score, phq_score, date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, gad_score, phq_score, date))
    conn.commit()

# Store Journal Entry
def store_journal_entry(user_id, entry, sentiment, date):
    c.execute("INSERT INTO journal (user_id, entry, sentiment, date) VALUES (?, ?, ?, ?)", 
              (user_id, entry, sentiment, date))
    conn.commit()

# Store Chat Message
def store_chat_message(user_id, message, sentiment, date):
    c.execute("INSERT INTO chat (user_id, message, sentiment, date) VALUES (?, ?, ?, ?)", 
              (user_id, message, sentiment, date))
    conn.commit()

# Store Mood
def store_mood(user_id, mood_score, date):
    c.execute("INSERT INTO mood (user_id, date, mood_score) VALUES (?, ?, ?)", 
              (user_id, date, mood_score))
    conn.commit()

# Retrieve Mood Data
def get_mood(user_id):
    c.execute("SELECT date, mood_score FROM mood WHERE user_id=?", (user_id,))
    return c.fetchall()

# Retrieve Journal History
def get_user_journal_history(user_id):
    c.execute("SELECT entry, sentiment, date FROM journal WHERE user_id=?", (user_id,))
    return c.fetchall()

# Retrieve Chat History
def get_user_chat_history(user_id):
    c.execute("SELECT message, sentiment, date FROM chat WHERE user_id=?", (user_id,))
    return c.fetchall()

# Retrieve Questionnaire Data
def get_questionnaire_data(user_id):
    c.execute("SELECT date, gad_score, phq_score FROM questionnaire WHERE user_id=?", (user_id,))
    return c.fetchall()

# Cleanup
def close_db():
    conn.close()
