import flet as ft


def main(page: ft.Page):
    page.title = "Приложение для списка дел"
    page.data = 0

    def add_todo(e):
        todo = f"{task_input.value}, категория: {category_input.value}"
        print(todo)
        todo_list_area.controls.append(ft.Text(value=todo, size=30))
        page.data += 1
        task_input.value = ""
        category_input = ""
        todo_count_text.value = f"Всего {page.data} задач(а)"
        page.update()

    title = ft.Text(value="Список дел", size=33)
    task_input = ft.TextField(label="Введите задачу")
    category_input = ft.TextField(label="Введите категорию")
    add_button = ft.ElevatedButton("Добавить", on_click=add_todo)
    todo_count_text= ft.Text(value=f"Всего {page.data} задач(а)", size=28)
    todo_list_area = ft.Column()

    page.add(
        title, 
        task_input, 
        category_input, 
        add_button,
        todo_count_text,
        todo_list_area
    )


ft.app(main)