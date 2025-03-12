import sqlite3
from data import User, Income, Expense

conn = sqlite3.connect('data/moneytrack.db', check_same_thread=False)   #
c = conn.cursor()

conn.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                currency TEXT NOT NULL
                )"""
             )

conn.execute("""CREATE TABLE IF NOT EXISTS incomes(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL,
            tag TEXT NOT NULL,
            username TEXT,
            description VARCHAR(200),
            date VARCHAR(50) NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("id")
            )"""
             )

conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL,
            tag TEXT NOT NULL,
            username TEXT,
            description VARCHAR(200),
            date VARCHAR(50) NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("id")
            )"""
             )


def get_user(email):
    c.execute("SELECT * FROM users WHERE email = :email", {'email': email})
    user = c.fetchone()
    if user:
        return User(_id=user[0], username=user[1], email=user[2], currency=user[3])
    else:
        return None


def get_income(_id):
    c.execute("SELECT * FROM incomes WHERE id = :id", {'id': _id})
    income = c.fetchone()
    if income:
        return Income(
            _id=income[0],
            title=income[1],
            amount=income[2],
            tag=income[3],
            username=income[5],
            description=income[6],
            date=income[7],
            user_id=income[8]
        )


def get_expense(_id):
    c.execute("SELECT * FROM expenses WHERE id = :id", {'id': _id})
    expense = c.fetchone()
    if expense:
        return Income(
            _id=expense[0],
            title=expense[1],
            amount=expense[2],
            tag=expense[3],
            username=expense[5],
            description=expense[6],
            date=expense[7],
            user_id=expense[8]
        )


def get_all_incomes(user_id):

    c.execute("PRAGMA foreign_keys = ON")
    c.execute("SELECT * FROM incomes WHERE user_id = :user_id", {'user_id': user_id})
    incomes = c.fetchall()
    return [
        Income(
            _id=income[0],
            title=income[1],
            amount=income[2],
            tag=income[3],
            username=income[4],
            description=income[5],
            date=income[6],
            user_id=income[7]
        ) for income in incomes
    ]


def get_all_expenses(user_id):

    c.execute("PRAGMA foreign_keys = ON")
    c.execute("SELECT * FROM expenses WHERE user_id = :user_id", {'user_id': user_id})
    expenses = c.fetchall()
    return [
        Expense(
            _id=expense[0],
            title=expense[1],
            amount=expense[2],
            tag=expense[3],
            username=expense[4],
            description=expense[5],
            date=expense[6],
            user_id=expense[7]
        ) for expense in expenses
    ]


def add_user(user: User):
    with conn:
        c.execute("INSERT INTO users(username,email,currency) VALUES(:username, :email, :currency)",
                  {
                      "username": user.username,
                      "email": user.email,
                      "currency": user.currency
                  }
                  )


def update_currency(_id, currency):
    with conn:
        c.execute("UPDATE users SET currency = :amount WHERE id = :id",
                  {"currency": currency, "id": _id})


def add_income(income: Income):
    with conn:
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("""INSERT INTO incomes(title,amount,tag,username,description, date, user_id)
                  VALUES (:title, :amount, :tag, :username, :description, :date, :user_id)""",
                  {
                      "title": income.title,
                      "amount": income.amount,
                      "tag": income.tag,
                      "username": income.username,
                      "description": income.description,
                      "date": income.date,
                      "user_id": income.user_id
                  })


def add_expense(expense: Expense):
    with conn:
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("""INSERT INTO expenses(title,amount,tag,username,description, date, user_id)
                  VALUES (:title, :amount, :tag, :username, :description, :date, :user_id)""",
                  {
                      "title": expense.title,
                      "amount": expense.amount,
                      "tag": expense.tag,
                      "username": expense.username,
                      "description": expense.description,
                      "date": expense.date,
                      "user_id": expense.user_id
                  })


def update_income(_id: int,
                  title: str = None,
                  amount: int = None,
                  tag: str = None,
                  username: str = None,
                  description: str = None,
                  ):
    title_updated = title
    amount_updated = amount
    tag_updated = tag
    username_updated = username
    description_updated = description

    with conn:
        if title:
            c.execute(f"UPDATE incomes SET title = :title WHERE id = :id",
                      {"title": title_updated, "id": _id})
        if amount:
            c.execute(f"UPDATE incomes SET amount = :amount WHERE id = :id",
                      {"amount": amount_updated, "id": _id})
        if tag:
            c.execute(f"UPDATE incomes SET tag = :tag WHERE id = :id",
                      {"tag": tag_updated, "id": _id})

        if username:
            c.execute(f"UPDATE incomes SET username = :username WHERE id = :id",
                      {"username": username_updated, "id": _id})
        if description:
            c.execute(f"UPDATE incomes SET description = :description WHERE id = :id",
                      {"description": description_updated, "id": _id})


def update_expense(
        _id: int,
        title: str = None,
        amount: int = None,
        tag: str = None,
        username: str = None,
        description: str = None,
        ):
    title_updated = title
    amount_updated = amount
    tag_updated = tag
    username_updated = username
    description_updated = description

    with conn:
        if title:
            c.execute(f"UPDATE expenses SET title = :title WHERE id = :id",
                      {"title": title_updated, "id": _id})
        if amount:
            c.execute(f"UPDATE expenses SET amount = :amount WHERE id = :id",
                      {"amount": amount_updated, "id": _id})
        if tag:
            c.execute(f"UPDATE expenses SET tag = :tag WHERE id = :id",
                      {"tag": tag_updated, "id": _id})

        if username:
            c.execute(f"UPDATE expenses SET username = :username WHERE id = :id",
                      {"username": username_updated, "id": _id})
        if description:
            c.execute(f"UPDATE expenses SET description = :description WHERE id = :id",
                      {"description": description_updated, "id": _id})


def delete_income(_id):
    with conn:
        c.execute("DELETE from incomes WHERE  id = :id", {'id': _id})


def delete_expense(_id):
    with conn:
        c.execute("DELETE from expenses WHERE  id = :id", {'id': _id})
