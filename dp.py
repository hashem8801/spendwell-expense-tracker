import sqlite3

DB_NAME = 'expenses.db'


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        notes TEXT
        )    
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT NOT NULL
            )
        """)

    cur.execute("""
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('currency', 'KD')
        """)

    default_categories = [
        ("Food", "#FF6B6B"),
        ("Gas", "#4D96FF"),
        ("Shopping", "#A66CFF"),
        ("Bills", "#FFD93D"),
        ("Entertainment", "#A66CFE"),
        ("Other", "#6BCB77")
    ]

    cur.executemany("""
            INSERT OR IGNORE INTO categories (name, color)
            VALUES (?, ?)
        """, default_categories)

    conn.commit()
    conn.close()



def add_expense(amount, category, date, notes):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO expenses (amount, category, date, notes) 
    VALUES (?, ?, ?, ?)
    """, (amount, category, date, notes))

    conn.commit()
    conn.close()



def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("Select * from expenses")
    expenses = cur.fetchall()

    conn.close()
    return expenses


def delete_expense(id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id = ?", (id,))

    conn.commit()
    conn.close()



def get_currency():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT value FROM settings WHERE key = 'currency'")
    result = cur.fetchone()

    conn.close()
    return result[0] if result else "KD"


def update_currency(currency):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES ('currency', ?)
    """, (currency,))

    conn.commit()
    conn.close()


def get_categories():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id, name, color FROM categories")
    data = cur.fetchall()

    conn.close()
    return data


def add_category(name, color):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO categories (name, color)
        VALUES (?, ?)
    """, (name, color))

    conn.commit()
    conn.close()


def update_category(category_id, name, color):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE categories
        SET name = ?, color = ?
        WHERE id = ?
    """, (name, color, category_id))

    conn.commit()
    conn.close()