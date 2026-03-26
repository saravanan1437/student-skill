"""
auth.py — Authentication module for Student Career Matcher
Handles: SQLite DB setup, user registration, login validation, password hashing
"""

import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    """Create users and assessments tables if not exists."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            email   TEXT    NOT NULL,
            name    TEXT    NOT NULL,
            stream  TEXT    NOT NULL,
            board   TEXT    NOT NULL,
            career  TEXT    NOT NULL,
            match   INTEGER NOT NULL,
            date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_assessment(email: str, name: str, stream: str, board: str, career: str, match: int):
    """Save a student's assessment result."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO assessments (email, name, stream, board, career, match) VALUES (?, ?, ?, ?, ?, ?)",
        (email.lower(), name, stream, board, career, match)
    )
    conn.commit()
    conn.close()


def get_user_records(email: str):
    """Retrieve all history for a specific user."""
    conn = _get_conn()
    records = conn.execute(
        "SELECT name, stream, board, career, match, date FROM assessments WHERE email = ? ORDER BY date DESC",
        (email.lower(),)
    ).fetchall()
    conn.close()
    return records


def _hash_password(password: str) -> str:
    """SHA-256 hash of password with a fixed salt prefix for security."""
    salted = "career_matcher_salt_2024_" + password
    return hashlib.sha256(salted.encode()).hexdigest()


def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (True, "success") or (False, "error message").
    """
    if not name.strip():
        return False, "Name cannot be empty."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    try:
        conn = _get_conn()
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), _hash_password(password))
        )
        conn.commit()
        conn.close()
        return True, "success"
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists. Please login."


def login_user(email: str, password: str) -> tuple[bool, str]:
    """
    Validate login credentials.
    Returns (True, name) on success or (False, "error message") on failure.
    """
    if not email or not password:
        return False, "Please fill in all fields."

    conn = _get_conn()
    row = conn.execute(
        "SELECT name, password FROM users WHERE email = ?",
        (email.strip().lower(),)
    ).fetchone()
    conn.close()

    if row is None:
        return False, "No account found with this email. Please register first."

    stored_name, stored_hash = row
    if _hash_password(password) != stored_hash:
        return False, "Incorrect password. Please try again."

    return True, stored_name


# Initialize the database on import
init_db()
