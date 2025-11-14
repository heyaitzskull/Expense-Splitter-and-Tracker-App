from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import delete

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.jinja_env.add_extension('jinja2.ext.do')

db = SQLAlchemy(app)

# TO DO:
# DONE: 1. In the "My expenses" section, be able to click on each expense, 
#       taking you to a separate page for expenses. 
#       Here add a 
#           - "complete" button: it completes the task, changes comlpete: 0 to complete: 1 (to add to history)
#           - and "Pay Now" button where it reveals 3 buttons, Venmo, Cashapp, Paypall, 
#                   and zelle to redirect to the approproproate website
#   
# DONE: 2: Add a section of "Current Expenses" for all expenses assigned BY user so that they can edit or delete them

# DONE: 3: Add a history section where all users can see all of their expenses that they have completed, (when completed: 1)

# DECIDED NOT TO DO: 4: in each section, there should only be a limited number of expenses displayed, so add a
#    more button where it reveals the rest of the expenses. OR maybe a view all that takes u to its own page??

# 5: ON THIS STEP: CSS, style everything


# Future features possible to add:
# - home button and back button, and finish edit expense
# - DONE: ONLY owner of expense is able to edit + delete expense - tmr
# - number notification a couple hours before payment is due
# 
# 
# - assignees can request a change from the expense (cost or due date) to owner of expense
#   in which they can approve or disapprove(with option to add a note for a reason)
#       ~ if approved: variables change in database, assignee who requested is notified of change
#       ~ is denied: assignee who requested is notified of denial with possible note of reason
# - when adding expense, add a checkbox saying "split evenly" 
#       ~ where after user enters a cost AND assignees, the cost does the calculations and
#           automatically splits evenly + inputs this cost in the "cost" box


expense_assignments = db.Table('expense_assignments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('expense_id', db.Integer, db.ForeignKey('expense.id')) 
)

# Roommate database
class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    expenses = db.relationship('Expense', secondary=expense_assignments, backref='assigned_users')

    def __repr__(self):
        return f"Name {self.id}"

# Expense database
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(20))
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    assigned_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # assigned_by = db.Column(db.String(20))
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='created_expenses')

    
    due_by = db.Column(db.DateTime)
    note = db.Column(db.String(200))
    completed = db.Column(db.Integer, default=0) #1= true/complete, 0=false/incomplete

    def __repr__(self):
        return f"Expense {self.id}"


# Homepage
@app.route("/", methods=["POST", "GET"])
def index():

    #add a name
    if request.method == "POST":
        # getting the name that is typed into the form with id="name"
        curr_name = request.form['name']

        # creating a new name object
        new_name = User(name=curr_name)

        try:
            db.session.add(new_name)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    
    #see all names on display
    else:
        #storing all the names here
        names = User.query.order_by(User.created_on).all()

        # sending the variable "names" with all the names from database 
        # so that the html can use it
        return render_template("index.html", names=names)

# Delete a name
@app.route("/delete_name/<int:id>")
def deleteName(id:int):

    #getting user from User database with the given id
    delete_user = User.query.get_or_404(id)

    try:
        #used to be assigned_by=delete_user.name
        expenses_to_delete = Expense.query.filter_by(assigned_by_id=delete_user.id).all()
        for expense in expenses_to_delete:
            db.session.delete(expense)

        db.session.delete(delete_user)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

@app.route("/delete_expense/<int:user_id>/<int:expense_id>")
def delete_expense(user_id:int, expense_id:int):
    delete_ex = Expense.query.get_or_404(expense_id)

    try:
        db.session.delete(delete_ex)
        db.session.commit()
        return redirect(f"/my_expenses/{user_id}")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
@app.route("/edit_expense/<int:user_id>/<int:expense_id>", methods=["POST", "GET"])
def edit_expense(user_id:int, expense_id:int):
    user = User.query.get_or_404(user_id)
    edit_ex = Expense.query.get_or_404(expense_id)
    all_names = User.query.order_by(User.created_on).all() 

    #need to send all users assigned to the edit_expense
    assigned_users = edit_ex.assigned_users

    if request.method == "POST":

        edit_ex.title = request.form.get("expense_name")
        edit_ex.cost = request.form.get("expense_cost")
        due_by_str = request.form.get("due_by")
        edit_ex.due_by = datetime.strptime(due_by_str, '%Y-%m-%d') if due_by_str else None
        edit_ex.note = request.form.get("note")
        

        new_assigned_ids = request.form.getlist("assign[]")
        

        try:
            db.session.execute(
                delete(expense_assignments).where(expense_assignments.c.expense_id == expense_id)
            )
    
            # assigning each user the expense
            for uid in new_assigned_ids:
                assigned_user = User.query.get(int(uid))
                if assigned_user:
                    edit_ex.assigned_users.append(assigned_user)

            db.session.commit()
            return redirect(f"/my_expenses/{user_id}")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template("add_expense.html", 
                                user=user, edit_ex=edit_ex, 
                                all_names=all_names,
                                assigned_users=assigned_users)
    

# Edit a name
@app.route("/edit_name/<int:id>", methods=['GET', 'POST'])
def edit_name(id:int):

    #getting user from User database with the given id
    edit_name = User.query.get_or_404(id)

    #this POST is for what is displayed after you edit everything
    if request.method == "POST":
        #updating the name of the user in the database
        edit_name.name = request.form['name']
        try:
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        
    #else is for when you CLICK on edit
    else:
        return render_template("edit_name.html", names=edit_name)


@app.route("/dashboard/<int:id>", methods=["POST", "GET"])
def dashboard(id:int):

    user = User.query.get_or_404(id)
    all_expenses = user.expenses

    if request.method == "POST":
        return redirect(f"/dashboard/{id}")
    else:
        return render_template("dashboard.html", user=user, all_expenses=all_expenses)


@app.route("/add_expense/<int:id>", methods=["POST", "GET"])
def add_expense(id:int):

    # the user that was clicked, we are on this user's dashboard rn
    user = User.query.get_or_404(id)

    # for selecting roommates when adding expenses
    all_names = User.query.order_by(User.created_on).all() 

    if request.method == "POST":

        # user = User.query.get_or_404(id)

        title = request.form.get("expense_name")
        print(title)
        cost = request.form.get("expense_cost")
        print(cost)
        due_by_str = request.form.get("due_by")
        due_by = datetime.strptime(due_by_str, '%Y-%m-%d') if due_by_str else None
        note = request.form.get("note")

        assigned_ids = request.form.getlist("assign[]")

        new_expense = Expense (
            title = title,
            cost = cost,
            assigned_by_id=user.id,
            due_by = due_by,
            note = note
        )

        try:

            # assigning each user the expense
            for uid in assigned_ids:
                assigned_user = User.query.get(int(uid))
                if assigned_user:
                    new_expense.assigned_users.append(assigned_user)
            
            db.session.add(new_expense)
            db.session.commit()
            return redirect(f"/dashboard/{id}")

        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    

    # when you CLICK on add expense button
    else:
        return render_template("add_expense.html", 
                               all_names=all_names,
                               user=user)

@app.route("/expense_view/<int:user_id>/<int:expense_id>")
def expense_view(user_id:int, expense_id:int):

    user = User.query.get_or_404(user_id)
    expense = Expense.query.get_or_404(expense_id)

    try:
        return render_template("expense_view.html", user=user, expense=expense)
    except Exception as e:
        print(f"Error: {e}")
        return f"ERROR: {e}"
    
@app.route("/complete/<int:user_id>/<int:expense_id>", methods=["POST"])
def complete(user_id:int, expense_id:int):

    user = User.query.get_or_404(user_id)
    expense = Expense.query.get_or_404(expense_id)
    
    expense.completed = 1
    db.session.commit()

    try:
        return redirect(f"/dashboard/{user_id}")
    except Exception as e:
        print(f"Error: {e}")
        return f"ERROR: {e}"

@app.route("/my_expenses/<int:user_id>")
def my_expenses(user_id:int):
    user = User.query.get_or_404(user_id)
    user_expenses = Expense.query.filter_by(assigned_by_id=user.id).order_by(Expense.assigned_on).all()

    try:
        return render_template("my_expenses.html", user=user, expenses=user_expenses)
    except Exception as e:
        print(f"Error: {e}")
        return f"ERROR: {e}"

# bugs(count: 2), customize (count: 1):
# ----------------------------------------------------------
# FIXED!!!!!! when assigning an expense, if a user has the same name as another user, it should only assigns to the first user with that name
# however, when a user has the same name as another user, its expenses are all mixed together
# is fixable by either: making sure no two users can have the same name
# OR by changing the way expenses are assigned to users (by id instead of name)  <- perferrably this one

# DONEEEE: BUG2: in the home page, when clicking on a name/edit/delete to go to their dashboard, you HAVE to click on the letters.
# make it so that the whole box is clickable58

# customize err message for required fields when adding/editing an expense  
# cant do: make calendar pop up prettier when selecting due date
# DONE: make edit, due by, and assign to boxes prettier
# ----------------------------------------------------------

# thing to add maybe:
# did but music refreshes every new page so i might remove it ::: music -> able to turn on and off *yes-
# back button *yes - try today ?
# lady who changes expression on each page *maybe later


# run env: .\env\Scripts\Activate
# run app: python app.py



if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)