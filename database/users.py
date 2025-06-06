import sqlite3
import bcrypt as bc
from states import constants as c


def validate_password(password:str) -> bool:
    if not all(ord(char) >= 32 and ord(char) <= 126 for char in password):
        return False
    return True

def hash_password(password:str) -> hex:
    salt = bc.gensalt()
    hashed = bc.hashpw(password.encode('utf-8'), salt)
    return hashed

def new_user(username, password, privilege=1) -> None:
    db = sqlite3.connect(c.DATABASE_PATH)
    cursor = db.cursor()

    try:
        password = hash_password(password)
        cursor.execute("INSERT IF NOT EXISTS INTO USERS (username, password, privilege) VALUES (?, ?, ?)", (username, password, privilege))
        db.commit()
    except Exception:
        return
    finally:
        db.close()
        cursor.close()

def delete_user(username:str) -> None:
    db = sqlite3.connect(c.DATABASE_PATH)
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM USERS WHERE username = ?", (username,))
    except Exception:
        #user not found
        db.close()
        cursor.close()
    finally:
        db.close()
        cursor.close()

def user_login(username, password) -> bool:
    db = sqlite3.connect(c.DATABASE_PATH)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT password FROM USERS WHERE username = ?", (username,))
        password2 = cursor.fetchone()[0]

        if password2 is None: #user not found
            return False

        if bc.checkpw(password.encode('utf-8'), password2):
            return True
        else:
            return False
    except Exception:
        return False
    finally:
        db.close()
        cursor.close()
