import sqlite3

DB_NAME = "notifier.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # User table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        age INTEGER,
        income INTEGER,
        state TEXT
    )
    ''')

    # Policies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        min_age INTEGER,
        max_age INTEGER,
        max_income INTEGER,
        state TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Tables created successfully")