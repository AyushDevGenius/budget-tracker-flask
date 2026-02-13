from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)

# YHA DATABASE CONNECT KR RHE 
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR PASSWORD",   # MY SQL KA PASSWORD
        database="budget_tracker_1"
    )
# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")

# ENTRY PAGE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        entry_type = request.form["type"]
        month = request.form["month"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expenses (amount, category, type, month) VALUES (%s, %s, %s, %s)",
            (amount, category, entry_type, month)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/summary")

    return render_template("add.html")

# -------- SUMMARY PAGE --------
@app.route("/summary")
def summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Income
    cursor.execute("SELECT SUM(amount) AS total_income FROM expenses WHERE type='income'")
    income_result = cursor.fetchone()
    income = income_result["total_income"] if income_result["total_income"] else 0

    # Total Expense
    cursor.execute("SELECT SUM(amount) AS total_expense FROM expenses WHERE type='expense'")
    expense_result = cursor.fetchone()
    expense = expense_result["total_expense"] if expense_result["total_expense"] else 0

    balance = income - expense

    cursor.close()
    conn.close()

    return render_template("summary.html", income=income, expense=expense, balance=balance)

if __name__ == "__main__":
    app.run(debug=True)




