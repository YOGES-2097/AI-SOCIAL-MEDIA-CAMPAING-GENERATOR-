import sqlite3
import os

DB_NAME = "ai_media.db"

def init_db():
    """Creates the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            campaign_topic TEXT,
            generated_content TEXT,
            target_platform TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # This allows us to access columns by name (like dictionaries)
    return conn