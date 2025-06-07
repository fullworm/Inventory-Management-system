import sqlite3
import bcrypt as bc
from database import database_func as db


def validate_password(password:str) -> bool:
    if not all(32 <= ord(char) <= 126 for char in password):
        return False
    return True

def hash_password(password:str) -> hex:
    salt = bc.gensalt()
    hashed = bc.hashpw(password.encode('utf-8'), salt)
    return hashed

def new_user(username, password, privilege=1) -> None:
    with db.get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            password = hash_password(password)
            cursor.execute("INSERT IF NOT EXISTS INTO USERS (username, password, privilege) VALUES (?, ?, ?)", (username, password, privilege))
            conn.commit()
        except Exception:
            return

def delete_user(username:str) -> None:
    with db.get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM USERS WHERE username = ?", (username,))
            conn.commit()
        except Exception:
            return

def user_login(username, password) -> bool:
    with db.get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password FROM USERS WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result is None:  # user not found
                return False

            password2 = result[0]
            return bc.checkpw(password.encode('utf-8'), password2)

        except Exception:
            return False
