import sqlite3
import os
from contextlib import contextmanager
from states import constants as c

@contextmanager
def get_db_connection():
    os.makedirs(os.path.dirname(c.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(c.DATABASE_PATH)

    try:
        yield conn
    finally:
        conn.close()



def setup_database():
    # Delete the old database file if it exists
    if os.path.exists(c.DATABASE_PATH):
        os.remove(c.DATABASE_PATH)

    with get_db_connection() as conn:  # Added parentheses here
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
                          (
                              id        INTEGER PRIMARY KEY AUTOINCREMENT not null,
                              username  TEXT                              not null,
                              password  TEXT                              not null,
                              privilege INTEGER
                          )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY
                          (
                              id           INTEGER PRIMARY KEY AUTOINCREMENT,
                              product_name TEXT    not null,
                              amount       INTEGER not null,
                              price        INTEGER not null,
                              type         TEXT    not null
                          )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS ORDERS
                          (
                              id      INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER
                          )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS ORDER_ITEMS
                          (
                              id           INTEGER PRIMARY KEY AUTOINCREMENT,
                              order_id     INTEGER not null,
                              product_name TEXT    not null,
                              FOREIGN KEY (order_id) REFERENCES ORDERS (id)
                          )''')

        conn.commit()


def view_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:", [table[0] for table in tables])

def reset_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Users;")
        cursor.execute("DROP TABLE IF EXISTS INVENTORY;")
        cursor.execute("DROP TABLE IF EXISTS ORDERS;")
        cursor.execute("DROP TABLE IF EXISTS ORDER_ITEMS;")
        cursor.commit()


def print_users():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        users = cursor.fetchall()
        print("Users in database:", users)

