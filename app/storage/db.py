import sqlite3
import os

DB_FILE = 'orders.db'

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_name TEXT,
            phone TEXT,
            garments_json TEXT,
            total INTEGER,
            status TEXT,
            created_at TEXT,
            notes TEXT,
            status_history TEXT,
            estimated_delivery_date TEXT,
            last_updated TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sequence (
            name TEXT PRIMARY KEY,
            seq INTEGER
        )
    ''')
    c.execute("INSERT OR IGNORE INTO sequence (name, seq) VALUES ('order_id', 1)")
    conn.commit()
    conn.close()

# Initialize DB on load
init_db()
