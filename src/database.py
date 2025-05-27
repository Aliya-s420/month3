import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        self.conn.commit()

    def add_expense(self, name, amount):
        self.cur.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (name, float(amount)))
        self.conn.commit()

    def delete_expense_by_id(self, expense_id):
        self.cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    def update_expense(self, expense_id, name, amount):
        self.cur.execute(
            "UPDATE expenses SET name = ?, amount = ? WHERE id = ?",
            (name, float(amount), expense_id)
        )
        self.conn.commit()

    def get_expense_by_id(self, expense_id):
        self.cur.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        return self.cur.fetchone()

    def all_expenses(self):
        self.cur.execute("SELECT * FROM expenses")
        return self.cur.fetchall()

    def total_expenses(self):
        self.cur.execute("SELECT SUM(amount) FROM expenses")
        result = self.cur.fetchone()[0]
        return round(result, 2) if result else 0.0