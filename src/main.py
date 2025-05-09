import flet as ft


def main(page: ft.Page):
    page.title = "Учет расходов"

    title = ft.Text(value="Ваши расходы", size=30)
    name1_input = ft.TextField(label="Название расхода")
    name2_input = ft.TextField(label="Сумма расхода")
    button = ft.ElevatedButton("Добавить")

    page.add(title, name1_input, name2_input, button)


ft.app(main)
