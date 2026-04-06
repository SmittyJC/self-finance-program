# ------------------------------------------------------------
# File: init_db.py
# Date: April 2026
# Authors:
#   - Karan Gosai
#   - Michael Groves
#   - Kamal Al Shawa
#   - James Smith
#
# Description:
#   Initializes the SQLite database and creates all required
#   tables for users, categories, and transactions.
# ------------------------------------------------------------

import sqlite3

connection = sqlite3.connect("finance.db")
cursor = connection.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

# Categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
""")

# Transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    category_id INTEGER,
    type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
""")

# Default categories
default_categories = [
    # Income Categories
    "Paycheck",
    "Support",
    "Bonus",
    "Reimbursement",
    "Investment Income",
    "Other Income",

    # Expense Categories
    "Mortgage/Rent",
    "Auto Payment",
    "Insurance",
    "Electric",
    "Gas",
    "Water/Trash",
    "Internet/Network",
    "Phone Bill",
    "Groceries",
    "Fuel",
    "Debt/Credit Cards",
    "Subscriptions",
    "Entertainment",
    "Dining Out",
    "Medical/Health",
    "Savings",
    "Miscellaneous"
]

for category in default_categories:
    cursor.execute(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)",
        (category,)
    )

connection.commit()
connection.close()

print("Database initialized successfully.")