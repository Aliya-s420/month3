# import flet as ft


# def main(page: ft.Page):
#     page.title = "Приложение для списка дел"

#     def change_name(e):
#         if name_input.value:
#             title.value = f"Привет", {name_input.value}
#             title.value = ""
#         else:
#             title.value = "Привет, мир"

#         page.update()

#     title = ft.Text(value="Привет мир!", size=30)
#     task_input = ft.TextField(label="Введите имя")
#     name_input = ft.TextField(label="Введите категорию")
#     add_button = ft.ElevatedButton("Добавить", on_click=change_name)
#     todo_list_area = ft.Column()

#     page.add(title, task_input, name_input, add_button, todo_list_area)


# ft.app(main)


import flet as ft

from database import Database


def main(page: ft.Page):
    page.title = "Учет расходов"
   
    page.data = 0

    db = Database("db.sqlite3")
    
    db.create_tables()

    todos = db.all_todos()
    print(todos)

    def add_todo(e):
        db.add_todo(task=task_input.value, amount=amount_input.value)

        amount_sum = float(amount_input.value)

        todo_list_area.controls.clear()
        todos = db.all_todos()
        for todo in todos:
            todo_list_area.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(value=f"Расход: {todo[1]}", size=30),
                        ft.Text(value=f"Сумма: {todo[2]}", size=30),
                    ]
                )
            )
            page.data += amount_sum

        task_input.value = ""
        amount_input.value = ""
        todo_count_text.value = f"Общая сумма расходов {page.data} (сом)"

        page.update()

    title = ft.Text(value="Ваши расходы", size=33)
    task_input = ft.TextField(label="Название расходов")
    amount_input = ft.TextField(label="Сумма расходов (сом)")
    add_button = ft.ElevatedButton("Добавить", on_click=add_todo)
    todo_count_text = ft.Text(value=f"Общая сумма расходов {page.data} (сом)", size=24)
    todo_list_area = ft.Column()
    form_area = ft.Row(controls=[task_input, amount_input, add_button])
    title.value = "Ваши расходы"

    page.add(
        title,
        form_area,
        todo_count_text,
        todo_list_area,
    )

ft.app(main)