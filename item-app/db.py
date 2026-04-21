import sqlite3
from flask import g

DB_PATH = "app.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)

    sample_items = [
        ("Sword",),
        ("Shield",),
        ("Potion",),
        ("Helmet",),
        ("Boots",),
        ("Ring",),
        ("Bow",),
        ("Arrow",)
    ]

    cur.execute("SELECT COUNT(*) FROM items")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO items (name) VALUES (?)", sample_items)

    users = [
        ("admin", "Monl4u_P4ssw0rD_2026"),
        ("alice", "password123"),
        ("bob", "qwerty"),
        ("charlie", "letmein"),
    ]

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        for user in users:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                user
            )

    db.commit()
    db.close()

