import sqlite3
import os
from contextlib import contextmanager
from states import constants as c

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(c.DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()



def setup_database():
    # Delete the old database file if it exists
    if c.DATABASE_PATH:
        os.remove(c.DATABASE_PATH)

    with get_db_connection as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
            (id INTEGER PRIMARY KEY AUTOINCREMENT not null, 
            username TEXT not null, 
            password TEXT not null, 
            privilege INTEGER)''')

        #remember that the prices are multiplied by 100 to keep simplicity. When you calculate prices, divide by that
        cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            product_name TEXT not null, 
            amount INTEGER not null, 
            price INTEGER not null)''')

        #ORDERS is connected to ORDER_ITEMS, because apparently it's the way I should do things if I want to have a list in SQL
        cursor.execute('''CREATE TABLE IF NOT EXISTS ORDERS 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS ORDER_ITEMS 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            order_id INTEGER not null, 
            product_name TEXT not null, 
            FOREIGN KEY (order_id) REFERENCES ORDERS (id))''')

        cursor.commit()

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

