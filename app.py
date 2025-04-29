from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='expense'
)
cursor = conn.cursor(dictionary=True)

# Home - Read
@app.route('/')
def index():
    # Fetch all expenses
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    # Fetch total amount directly from database
    cursor.execute("SELECT SUM(amount) AS total FROM expenses")
    result = cursor.fetchone()
    total_amount = result['total'] if result['total'] else 0.0

    return render_template('index.html', expenses=expenses, total_amount=total_amount)

# Create
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']

        try:
            amount = float(amount)
        except ValueError:
            amount = 0.0

        cursor.execute("INSERT INTO expenses (description, amount, dates) VALUES (%s, %s, %s)", (description, amount, date))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Update
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']

        try:
            amount = float(amount)
        except ValueError:
            amount = 0.0

        cursor.execute("UPDATE expenses SET description=%s, amount=%s, dates=%s WHERE id=%s", (description, amount, date, id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM expenses WHERE id=%s", (id,))
    expense = cursor.fetchone()
    return render_template('edit.html', expense=expense)

# Delete
@app.route('/delete/<int:id>')
def delete_expense(id):
    cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
