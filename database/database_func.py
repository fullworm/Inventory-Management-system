import sqlite3
import os
from contextlib import contextmanager


DATABASE_PATH = "database.sql"
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()




def setup_database():
    # Delete the old database file if it exists
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
                          (
                              id        INTEGER PRIMARY KEY AUTOINCREMENT not null,
                              username  TEXT                              not null,
                              password  TEXT                              not null,
                              privilege INTEGER
                          )''')
        #remember that prices are multiplied by 100 to store them as an integer
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
                              id       INTEGER PRIMARY KEY AUTOINCREMENT,
                              name     TEXT not null,
                              finished BOOLEAN default 0,
                              total_price REAL not null,
                              date     TEXT    not null
                          )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS ORDER_ITEMS
                          (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              order_id INTEGER,
                              product_name TEXT,
                              quantity INTEGER,
                              price REAL,
                              FOREIGN KEY(order_id) REFERENCES orders(id)
                          )''')

        conn.commit()
    create_test_data_inv()


def view_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:", [table[0] for table in tables])

def reset_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS USERS;")
        cursor.execute("DROP TABLE IF EXISTS INVENTORY;")
        cursor.execute("DROP TABLE IF EXISTS ORDERS;")
        cursor.execute("DROP TABLE IF EXISTS ORDER_ITEMS;")
        conn.commit()
    setup_database()

def print_users():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        users = cursor.fetchall()
        print("Users in database:", users)


def create_test_data_inv():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO INVENTORY (product_name, amount, price, type) VALUES (?,?,?,?)", ("pan", 100, 100, "food"))
        cursor.execute("INSERT INTO INVENTORY (product_name, amount, price, type) VALUES (?,?,?,?)", ("tomato", 100, 100, "food"))
        cursor.execute("INSERT INTO INVENTORY (product_name, amount, price, type) VALUES (?,?,?,?)", ("sandwich", 100, 100, "food"))
        cursor.execute("INSERT INTO INVENTORY (product_name, amount, price, type) VALUES (?,?,?,?)", ("mofongo", 100, 100, "food"))
        conn.commit()  # Add this line to commit the changes
        for v in cursor.execute("SELECT * FROM INVENTORY").fetchall():
            print(v)
def table_read():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM INVENTORY")
        tables = cursor.fetchall()
        print("Tables in database:", tables)





