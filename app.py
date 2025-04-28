from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory store for expenses
expenses = []

@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = request.form['amount']
    date = request.form['date']

    # 🔥 Very important: Convert amount to float
    try:
        amount = float(amount)
    except ValueError:
        amount = 0.0

    expense = {
        'description': description,
        'amount': amount,
        'date': date
    }
    expenses.append(expense)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
