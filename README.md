# Expense Splitter and Tracker App
Created by: Prativa Khatiwada

A web application to help roommates manage and split expenses efficiently, with support for external payment redirects.

### Technologies

Backend: Flask, SQLAlchemy<br>
Frontend: HTML, SASS, JavaScript<br>
Database: Relational (SQLite/PostgreSQL)<br>

### Features

Add and manage roommates and their expenses<br>
Assign expenses with details like cost, due date, and assignees<br>
Filter-view current and past expenses per roommate<br>
Support for external payment redirects (Venmo, Zelle, Cash App, PayPal)<br>
RESTful API supporting CRUD operations and secure session management

### Installation

**Clone the repository:**
git clone <repository_url><br>
cd expense-tracker

**Create a virtual environment and install dependencies:**
python -m venv venv<br>
source venv/bin/activate  (On Windows: venv\Scripts\activate)<br>
pip install -r requirements.txt

**Run the Flask application:**
flask run
