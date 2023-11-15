
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

# Configure the database connection URI
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:mypassword@expensesdb.chqcr0joe65n.eu-west-1.rds.amazonaws.com/expensesdb'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy instance
db = SQLAlchemy(application)

# Define a model for your data
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    income = db.Column(db.Float)
    outcome = db.Column(db.Float)
    balance = db.Column(db.Float)

# Function to create database tables
def create_tables():
    with application.app_context():
        db.create_all()

# Create the database tables
create_tables()


@application.route('/')
def get_statistics():
    expenses = Expense.query.all()

    # Calculate the total balance by summing up income and subtracting outcome
    total_balance = sum((expense.income - expense.outcome) for expense in expenses)

    return render_template('statistics1.html', data=expenses, total_balance=total_balance)


@application.route('/', methods=['POST'])
def add_data():
    # Get data from the form
    date = request.form.get('Date')
    details = request.form.get('Details')
    income = float(request.form.get('In'))
    outcome = float(request.form.get('Out'))

    # Calculate the balance
    balance = income - outcome

    # Create a new Expense object
    new_expense = Expense(date=date, details=details, income=income, outcome=outcome, balance=balance)

    # Add the new expense to the database
    db.session.add(new_expense)
    db.session.commit()

    # Redirect back to the main page
    return redirect(url_for('get_statistics'))

@application.route('/update/<int:entry_id>', methods=['POST'])
def update_data(entry_id):
    # Get the updated data from the form
    date = request.form.get('Date')
    details = request.form.get('Details')
    income = float(request.form.get('In'))
    outcome = float(request.form.get('Out'))

    # Calculate the balance
    balance = income - outcome

    # Find the entry with the matching ID and update its data
    updated_expense = Expense.query.get(entry_id)
    if updated_expense:
        updated_expense.date = date
        updated_expense.details = details
        updated_expense.income = income
        updated_expense.outcome = outcome
        updated_expense.balance = balance

        # Commit the changes to the database
        db.session.commit()

    # Redirect back to the main page
    return redirect(url_for('get_statistics'))

@application.route('/delete/<int:entry_id>', methods=['GET'])
def delete_data(entry_id):
    # Find and remove the entry with the matching ID
    deleted_expense = Expense.query.get(entry_id)
    if deleted_expense:
        db.session.delete(deleted_expense)
        db.session.commit()


    # Redirect back to the main page
    return redirect(url_for('get_statistics'))




if __name__ == '__main__':
    application.run(debug=True)
