import sqlite3


class Database:
    """
    Класс для работы с БД. тут будут методы для создания таблиц,
    для добавления, обновления и удаления задач(таблица expenses)
    """

    def __init__(self, path):
        self.path = path

    def create_tables(self):
        """
        Метод, в котором описывается, какие таблицы и с какими колонками создаются для приложения
        """

        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount INTEGER
                )
            """)

    def all_todos(self):
        """
        Метод, в котором вызывается запрос для получения всех расходов из БД
        """

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM expenses")
            return result.fetchall()

    def add_todo(self, task: str, amount: str):
        """
        Метод, в котором вызывается запрос для добавления в БД нового расхода
        """

        try:
            float_amount = float(amount)
            with sqlite3.connect(self.path) as conn:
                conn.execute(
                    """
                    INSERT INTO expenses (name, amount) VALUES (?, ?)
                    """,
                    (task, float_amount),
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении расхода: {e}")
            return False

    def get_total_amount(self):
        """
        Метод для подсчета общей суммы всех расходов
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT SUM(amount) FROM expenses")
            total = result.fetchone()[0]
            return total if total else 0