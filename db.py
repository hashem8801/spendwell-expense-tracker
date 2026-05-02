# =====================================================
# imports
# =====================================================

import sqlite3


# =====================================================
# database name
# =====================================================

DB_NAME = 'expenses.db'


# =====================================================
# create database tables
# =====================================================

def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create expenses table to store transactions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        notes TEXT
        )    
    """)

    # Create settings table to store app settings like currency
    cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

    # Create categories table to store category names and colors
    cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT NOT NULL
            )
        """)

    # Add default currency if it does not already exist
    cur.execute("""
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('currency', 'KD')
        """)

    # Default categories shown when the app starts
    default_categories = [
        ("Food", "#FF6B6B"),
        ("Gas", "#4D96FF"),
        ("Shopping", "#A66CFF"),
        ("Bills", "#FFD93D"),
        ("Entertainment", "#A66CFE"),
        ("Other", "#6BCB77")
    ]

    # Insert default categories only if they do not already exist
    cur.executemany("""
            INSERT OR IGNORE INTO categories (name, color)
            VALUES (?, ?)
        """, default_categories)

    # Save changes and close the connection
    conn.commit()
    conn.close()


# =====================================================
# add new expense
# =====================================================

def add_expense(amount, category, date, notes):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Insert a new transaction into the expenses table
    cur.execute("""
    INSERT INTO expenses (amount, category, date, notes) 
    VALUES (?, ?, ?, ?)
    """, (amount, category, date, notes))

    # Save changes and close connection
    conn.commit()
    conn.close()


# =====================================================
# get all expenses
# =====================================================

def get_expenses():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get all rows from the expenses table
    cur.execute("Select * from expenses")
    expenses = cur.fetchall()

    # Close connection and return data
    conn.close()
    return expenses


# =====================================================
# delete expense by id
# =====================================================

def delete_expense(id):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Delete one transaction using its id
    cur.execute("DELETE FROM expenses WHERE id = ?", (id,))

    # Save changes and close connection
    conn.commit()
    conn.close()


# =====================================================
# get selected currency
# =====================================================

def get_currency():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Read the currency value from the settings table
    cur.execute("SELECT value FROM settings WHERE key = 'currency'")
    result = cur.fetchone()

    # Close connection
    conn.close()

    # Return saved currency, or KD if no currency exists
    return result[0] if result else "KD"


# =====================================================
# update selected currency
# =====================================================

def update_currency(currency):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Update the currency setting
    cur.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES ('currency', ?)
    """, (currency,))

    # Save changes and close connection
    conn.commit()
    conn.close()


# =====================================================
# get all categories
# =====================================================

def get_categories():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get category id, name, and color
    cur.execute("SELECT id, name, color FROM categories")
    data = cur.fetchall()

    # Close connection and return categories
    conn.close()
    return data


# =====================================================
# add new category
# =====================================================

def add_category(name, color):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Add a new category if it does not already exist
    cur.execute("""
        INSERT OR IGNORE INTO categories (name, color)
        VALUES (?, ?)
    """, (name, color))

    # Save changes and close connection
    conn.commit()
    conn.close()


# =====================================================
# update category name and color
# =====================================================

def update_category(category_id, name, color):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Update the selected category
    cur.execute("""
        UPDATE categories
        SET name = ?, color = ?
        WHERE id = ?
    """, (name, color, category_id))

    # Save changes and close connection
    conn.commit()
    conn.close()
