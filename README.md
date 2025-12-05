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

**Clone the repository:** <br>
git clone <repository_url><br>
cd expense-tracker

**Create a virtual environment and install dependencies:** <br>
python -m venv venv<br>
source venv/bin/activate  (On Windows: venv\Scripts\activate)<br>
pip install -r requirements.txt

**Run the Flask application:** <br>
flask run

bugs: when multiple users are assigned the same bill, when ONE user marks it complete, it sets it complete for EVERYONE. need to fix.

## Homepage
<img width="3840" height="1874" alt="image" src="https://github.com/user-attachments/assets/18f65889-16f4-487a-bbc3-1002a3788c67" />

## Adding an expense
<img width="3840" height="1874" alt="image" src="https://github.com/user-attachments/assets/df4efb8c-d90a-478d-97c5-8a79f579d15c" />

## Roommate dashboard
<img width="3840" height="1871" alt="image" src="https://github.com/user-attachments/assets/cd02060f-8318-4555-a1bf-8db6a4eedf46" />

## Expense detail

### Incomplete expense
<img width="3840" height="1872" alt="image" src="https://github.com/user-attachments/assets/a3c44898-484d-4e3b-a604-0cab4d277664" />
### clicking on "Pay Now" opens up payment method buttons that redirect you to the appropriate site
<img width="1056" height="323" alt="image" src="https://github.com/user-attachments/assets/43550b1b-0a16-4380-baae-269ba5fc0ea9" />
### Complete expense
<img width="3840" height="1860" alt="image" src="https://github.com/user-attachments/assets/d252a7e6-8cef-4be9-a266-7858986ff41e" />

## Roommate assigned expenses
<img width="3840" height="1862" alt="image" src="https://github.com/user-attachments/assets/16613c16-642f-49f2-8247-e54e56e2d693" />



