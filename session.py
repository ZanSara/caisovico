
from flask import session
from config import DATABASE_PATH
import sqlite3


def login(name, passw):
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        user = list(conn.execute("SELECT * FROM users WHERE username = ?", ([name])))
        if user:
            if user[0][1] != passw:       # Suppose that I will get only one user with this username
                return "Invalid password"
            session["logged_in"] = True
            session["username"] = user[0][0]
            return
        return "Invalid username"


def logout():
    if not session.pop("logged_in", None):
        return "Errore durante il logout."
    return

