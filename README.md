Project Title: Personal Finance Tracker (Flask + SQLite)

Overview:  
This project is a lightweight personal finance tracking application built using Python, Flask, and SQLite. It allows users to create accounts, log in securely, and record financial transactions such as income, expenses, gifts, and transfers. Each transaction stores a primary category selected by the user and supports a secondary refined category that can be assigned later through categorization logic. The application is designed to be modular, easy to extend, and suitable for team collaboration.

The software was developed in PyCharm because it provides excellent tools for managing Python virtual environments and dependencies. Using PyCharm helps ensure that packages remain consistent across machines and reduces the risk of version conflicts. Anyone running or extending this project should use a virtual environment and a reliable dependency‑management workflow.

Features
• User registration and secure login
• Session‑based authentication
• Add income and expense transactions
• Primary category selection (income, expense, gift, transfer)
• Support for secondary refined categories (such as Groceries, Rent, Utilities)
• SQLite database backend
• Modular structure for future analytics and dashboards
• Utility script for inspecting database contents

Technologies Used
• Python 3
• Flask web framework
• SQLite database
• Werkzeug for password hashing
• HTML templates using Jinja2
• PyCharm IDE for development and package management

Project Structure
The project contains the following main components:

• app.py – Main Flask application and route definitions
• init_db.py – Script to initialize the SQLite database and create required tables
• test_db.py – Utility script to inspect database contents
• finance.db – SQLite database file (created automatically)
• templates folder – Contains HTML templates such as login, dashboard, and transaction forms
• static folder – Contains optional CSS and JavaScript files

Database Schema
Users Table:  
Stores login credentials.
Fields include: id, username, password (hashed)

Transactions Table:  
Stores all financial entries for each user.
Fields include: id, user_id, amount, date, description, type (primary category), category_id (secondary category)

Categories Table:  
Stores refined category names such as Groceries, Rent, Utilities.
Fields include: id, name

This structure supports both user‑selected categories and more detailed categorization logic added later.

Installation and Setup
Install Python 3 if not already installed.

Create and activate a virtual environment to manage dependencies.

Install required packages such as Flask and Werkzeug.

Run the database initialization script (init_db.py) to create tables.

Start the application by running app.py.

Open a browser and navigate to http://127.0.0.1:5000 (127.0.0.1 in Bing) to access the site.
