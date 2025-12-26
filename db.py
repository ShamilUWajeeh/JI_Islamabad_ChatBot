import sqlite3
import pandas as pd
from datetime import datetime
import os

# RAILWAY LOGIC: Save DB to a permanent folder if online
if os.getenv("RAILWAY_ENVIRONMENT"):
    DB_FOLDER = "/app/data"
    os.makedirs(DB_FOLDER, exist_ok=True)
    DB_NAME = os.path.join(DB_FOLDER, "ji_election.db")
else:
    DB_NAME = "ji_election.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Candidates Table
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uc_number TEXT,
                    area_name TEXT,
                    candidate_name TEXT,
                    phone TEXT,
                    role TEXT DEFAULT 'General Member'
                )''')

    # 2. Knowledge Base Table (Editable Vision, Welcome Msgs, etc.)
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    content TEXT
                )''')

    # 3. Contacts (Users)
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    phone_number TEXT PRIMARY KEY,
                    name TEXT,
                    last_active DATETIME
                )''')

    # 4. Messages (Chat History)
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT,
                    sender TEXT,
                    content TEXT,
                    timestamp DATETIME,
                    FOREIGN KEY(phone_number) REFERENCES contacts(phone_number)
                )''')
    
    conn.commit()
    conn.close()
    print("Database Initialized/Updated!")

# --- Helper Functions ---

def run_query(query, params=()):
    """Runs a query that doesn't return data (INSERT, UPDATE, DELETE)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def get_data(query):
    """Runs a query that returns data (SELECT)"""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Run once to create DB
if __name__ == "__main__":
    init_db()