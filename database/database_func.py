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

def load_products():
        with get_db_connection() as db:
            new = []
            cursor = db.cursor()
            cursor.execute("SELECT * FROM INVENTORY")
            tables = cursor.fetchall()
            for row in tables:
                if row:
                    #price divided by 100 because it was stored as an integer by multiplying by 100
                    new.append([row[1], row[2], float(row[3])/100, row[4]])

            return new
        
def update_products(rowdata):
        with get_db_connection() as db:
            cursor = db.cursor()
            for p in rowdata:
                name = p[0]
                cursor.execute("SELECT COUNT(*) FROM INVENTORY WHERE product_name = ?", (name,))
                #prices are multiplied by 100 to keep them stored in the db as an integer
                if cursor.fetchone()[0] > 0:
                    cursor.execute("UPDATE INVENTORY SET amount = ?, price = ? WHERE product_name = ?", (p[1], p[2]*100, name))
                else:
                    #product thats been added and doesnt exist in the db yet
                    cursor.execute('INSERT INTO INVENTORY (product_name, amount, price, type)VALUES (?, ?, ?, ?)', (name, p[1], p[2]*100, p[3]))

            db.commit()










