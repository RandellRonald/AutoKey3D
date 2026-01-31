import sqlite3
import os
from datetime import datetime

DB_PATH = "backend/keys.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cut_depths TEXT NOT NULL,
            hash TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            stl_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_key(cut_depths: list[float], hash_val: str, stl_path: str):
    conn = get_db_connection()
    c = conn.cursor()
    # cut_depths saved as comma separated string
    cuts_str = ",".join(map(str, cut_depths))
    try:
        c.execute('''
            INSERT INTO keys (cut_depths, hash, stl_path)
            VALUES (?, ?, ?)
        ''', (cuts_str, hash_val, stl_path))
        conn.commit()
    except sqlite3.IntegrityError:
        # Should be checked before calling save_key, but handle just in case
        pass
    finally:
        conn.close()

def hash_exists(hash_val: str) -> bool:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM keys WHERE hash = ?', (hash_val,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_key(key_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM keys WHERE id = ?', (key_id,))
    key = c.fetchone()
    conn.close()
    return key
