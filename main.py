# ------------------------------------------------------------
# File: main.py
# Date: April 2026
# Authors:
#   - Karan Gosai
#   - Michael Groves
#   - Kamal Al Shawa
#   - James Smith
#
# Description:
#   Main Flask application handling routing, authentication,
#   session management, transaction submission,
#   monthly summaries, and viewing transactions.
# ------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import json

# Create a reusable database connection
def get_db_connection():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = "capstone_secret_key_2026"

# Category groups for dynamic dropdown filtering
CATEGORY_MAP = {
    "income": [
        "Paycheck",
        "Support",
        "Bonus",
        "Reimbursement",
        "Investment Income",
        "Other Income"
    ],
    "expense": [
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
    ],
    "transfer": [
        "Transfer"
    ],
    "gift": [
        "Gift"
    ]
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists.")
            conn.close()
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_pw)
        )

        conn.commit()
        conn.close()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            flash("User not recognized. Please check your username.", "error")
            return redirect(url_for("login"))

        if not check_password_hash(user["password"], password):
            flash("Incorrect password. Please try again.", "error")
            return redirect(url_for("login"))

        flash("Login successful. Welcome!", "success")
        session["user_id"] = user["id"]
        session["user"] = username

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=session["user"])


@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to add transactions.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        amount = request.form["amount"]
        date = request.form["date"]
        description = request.form["description"]
        type_ = request.form["type"]
        primary_category = request.form["category"]

        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM categories WHERE name = ?", (primary_category,))
        category_row = cursor.fetchone()

        if category_row is None:
            conn.close()
            flash("Selected category was not found.", "error")
            return redirect(url_for("add_transaction"))

        category_id = category_row[0]

        cursor.execute("""
            INSERT INTO transactions (user_id, amount, date, description, category_id, type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, amount, date, description, category_id, type_))

        conn.commit()
        conn.close()

        flash("Transaction added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "add_transaction.html",
        category_map=json.dumps(CATEGORY_MAP),
        default_categories=CATEGORY_MAP["income"]
    )


@app.route("/monthly_summary")
def monthly_summary():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in.", "error")
        return redirect(url_for("login"))

    selected_month = request.args.get("month")

    if not selected_month:
        selected_month = datetime.now().strftime("%Y-%m")

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, SUM(amount) as total
        FROM transactions
        WHERE user_id = ?
        AND strftime('%Y-%m', date) = ?
        GROUP BY type
    """, (user_id, selected_month))

    type_totals = cursor.fetchall()

    cursor.execute("""
        SELECT c.name as category, SUM(t.amount) as total
        FROM transactions t
        LEFT JOIN categories c
        ON t.category_id = c.id
        WHERE t.user_id = ?
        AND strftime('%Y-%m', t.date) = ?
        GROUP BY c.name
        ORDER BY total DESC
    """, (user_id, selected_month))

    category_totals = cursor.fetchall()

    conn.close()

    return render_template(
        "monthly_summary.html",
        selected_month=selected_month,
        type_totals=type_totals,
        category_totals=category_totals
    )


@app.route("/transactions")
def view_transactions():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view transactions.", "error")
        return redirect(url_for("login"))

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            t.amount,
            t.date,
            t.description,
            t.type,
            c.name AS category
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        ORDER BY t.date DESC, t.id DESC
    """, (user_id,))

    transactions = cursor.fetchall()
    conn.close()

    return render_template("view_transactions.html", transactions=transactions)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)