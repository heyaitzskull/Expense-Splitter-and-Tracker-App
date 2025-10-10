## Expense Splitter and Tracker App
# Created by: Prativa Khatiwada

A web application to help roommates manage and split expenses efficiently, with support for external payment redirects.

### Technologies

Backend: Flask, SQLAlchemy
Frontend: HTML, SASS, JavaScript
Database: Relational (SQLite/PostgreSQL)

### Features

Add and manage roommates and their expenses
Assign expenses with details like cost, due date, and assignees
Filter-view current and past expenses per roommate
Support for external payment redirects (Venmo, Zelle, Cash App, PayPal)
RESTful API supporting CRUD operations and secure session management

### Installation

**Clone the repository:**
git clone <repository_url>
cd expense-tracker

**Create a virtual environment and install dependencies:**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

**Run the Flask application:**
flask run
