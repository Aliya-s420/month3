import flet as ft

from database import Database


def main(page: ft.Page):
    page.title = "Учет расходов"
   
    db = Database("db.sqlite3")
    db.create_tables()

    # Получаем все расходы из базы данных
    expenses = db.all_todos()
    
    # Подсчитываем общую сумму при запуске
    total_amount = db.get_total_amount()

    def add_todo(e):
        # Проверяем, что поля не пустые
        if not task_input.value or not amount_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Заполните все поля"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Преобразуем строку в число
            amount_value = float(amount_input.value)
            
            # Добавляем расход в базу данных
            if db.add_todo(task=task_input.value, amount=amount_input.value):
                # Очищаем и обновляем список расходов
                update_expense_list()
                
                # Очищаем поля ввода
                task_input.value = ""
                amount_input.value = ""
                
                # Обновляем общую сумму
                update_total_amount()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Ошибка при добавлении расхода"))
                page.snack_bar.open = True
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Введите корректную сумму"))
            page.snack_bar.open = True
            
        page.update()

    def update_expense_list():
        """Обновляет список расходов"""
        expense_list_area.controls.clear()
        expenses = db.all_todos()
        for expense in expenses:
            expense_list_area.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(value=f"Расход: {expense[1]}", size=30),
                        ft.Text(value=f"Сумма: {expense[2]}", size=30),
                    ]
                )
            )

    def update_total_amount():
        """Обновляет общую сумму расходов"""
        total = db.get_total_amount()
        total_amount_text.value = f"Общая сумма расходов {total} (сом)"

    # Компоненты интерфейса
    title = ft.Text(value="Ваши расходы", size=33)
    task_input = ft.TextField(label="Название расходов")
    amount_input = ft.TextField(label="Сумма расходов (сом)")
    add_button = ft.ElevatedButton("Добавить", on_click=add_todo)
    total_amount_text = ft.Text(value=f"Общая сумма расходов {total_amount} (сом)", size=24)
    expense_list_area = ft.Column()
    
    # Размещаем поля ввода и кнопку в одну строку
    form_area = ft.Row(controls=[task_input, amount_input, add_button])

    # Заполняем список расходов при запуске
    update_expense_list()

    # Добавляем компоненты на страницу
    page.add(
        title,
        form_area,
        total_amount_text,
        expense_list_area,
    )


ft.app(main)