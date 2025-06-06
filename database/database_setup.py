import sqlite3
import os
from database import users as u
def setup_database():
    # Delete the old database file if it exists
    if os.path.exists('database.sql'):
        os.remove('database.sql')

    path = os.path.join('database', 'database.sql')
    database = sqlite3.connect(path)
    cursor = database.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
        (id INTEGER PRIMARY KEY AUTOINCREMENT not null, 
        username TEXT not null, 
        password TEXT not null, 
        privilege INTEGER)''')

    #remember that the prices are multiplied by 100 to keep simplicity. When you calculate prices divide by that
    cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTORY 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        product_name TEXT not null, 
        amount INTEGER not null, 
        price INTEGER not null)''')

    #ORDERS is connected to ORDER_ITEMS, because apparently its the way i should do things if i want to have list in sql
    cursor.execute('''CREATE TABLE IF NOT EXISTS ORDERS 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ORDER_ITEMS 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        order_id INTEGER not null, 
        product_name TEXT not null, 
        FOREIGN KEY (order_id) REFERENCES ORDERS (id))''')

    database.commit()
    database.close()
    cursor.close()


def view_tables():
    db = sqlite3.connect('database.sql')
    cursor = db.cursor()

    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", [table[0] for table in tables])
    u.new_user("admin", "admin")
    db.close()
    cursor.close()

def reset_database():
    db = sqlite3.connect('database.sql')
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users;")
    cursor.execute("DROP TABLE IF EXISTS INVENTORY;")
    cursor.execute("DROP TABLE IF EXISTS ORDERS;")
    cursor.execute("DROP TABLE IF EXISTS ORDER_ITEMS;")
    db.commit()
    db.close()

def print_users():
    db = sqlite3.connect('database.sql')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM USERS")
    users = cursor.fetchall()
    print("Users in database:", users)
