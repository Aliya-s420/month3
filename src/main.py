import flet as ft


def main(page: ft.Page):
    page.title = "Учет расходов"
    page.data = 0
    page.data = 0

    def add_todo(e):
        amount = float(category_input.value)
        todo = f"Расход:{task_input.value}/Сумма:{category_input.value} сом"
        print(todo)
        todo_list_area.controls.append(ft.Text(value=todo, size=30))

        page.data += amount

        task_input.value = ""
        category_input.value = ""
        todo_count_text.value = f"Общая сумма расходов: {page.data} сом"

        page.update()

    title = ft.Text(value="Ваши расходы", size=33)
    task_input = ft.TextField(label="Название расхода")
    category_input = ft.TextField(label="Сумма расхода(сом)")
    add_button = ft.ElevatedButton("Добавить", on_click=add_todo)
    todo_count_text = ft.Text(value=f"Общая сумма расходов {page.data} сом", size=28)
    todo_list_area = ft.Column()

    page.add(
        title,
        task_input,
        category_input,
        add_button,
        todo_count_text,
        todo_list_area,
    )


ft.app(main)