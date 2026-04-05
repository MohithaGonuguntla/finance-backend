from database import get_connection

#Users

def add_user(user):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, role, status) VALUES (?, ?, ?, ?)",
        (user.name, user.email, user.role, user.status)
    )
    connection.commit()
    connection.close()


def fetch_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    connection.close()
    return [dict(row) for row in data]


#Transactions

def add_transaction(txn):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO transactions 
        (amount, type, category, date, notes, user_id)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (txn.amount, txn.type, txn.category, txn.date, txn.notes, txn.user_id)
    )
    connection.commit()
    connection.close()


def fetch_transactions(type=None, category=None):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if type:
        query += " AND type=?"
        params.append(type)
    if category:
        query += " AND category=?"
        params.append(category)
    cursor.execute(query, params)
    data = cursor.fetchall()

    connection.close()
    return [dict(row) for row in data]


#Dashboard

def get_dashboard_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    total_income = sum(r["amount"] for r in rows if r["type"] == "income")
    total_expense = sum(r["amount"] for r in rows if r["type"] == "expense")
    category_summary = {}
    for r in rows:
        cat = r["category"]
        category_summary[cat] = category_summary.get(cat, 0) + r["amount"]

    connection.close()
    return {
    "total_income": total_income,
    "total_expense": total_expense,
    "net_balance": total_income - total_expense,
    "category_summary": category_summary
    }
