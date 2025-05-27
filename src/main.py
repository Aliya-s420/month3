import flet as ft
from database import Database

def main(page: ft.Page):
    page.title = "Приложение для учета расходов"
    page.window_width = 1024

    db = Database("db.sqlite3")
    db.create_tables()

    def get_rows() -> list[ft.Row]:
        rows = []
        for expense in db.all_expenses():
            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(value=str(expense[0])),
                        ft.Text(value=f"Расход: {expense[1]}", size=30),
                        ft.Text(value=f"Сумма: {expense[2]}", size=30, color=ft.colors.BLUE),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.colors.RED,
                            icon_size=20,
                            on_click=delete_expense,
                            data=expense[0],
                        ),
                    ]
                )
            )
        return rows

    def add_expense(e):
        db.add_expense(name=name_input.value, amount=amount_input.value)
        expense_list_area.controls = get_rows()
        name_input.value = ""
        amount_input.value = ""
        expense_count_text.value = f"Общая сумма расходов: {db.total_expenses()} сом"
        page.update()

    def delete_expense(e):
        db.delete_expense_by_id(expense_id=e.control.data)
        expense_list_area.controls = get_rows()
        expense_count_text.value = f"Общая сумма расходов: {db.total_expenses()} сом"
        page.update()

    title = ft.Text(value="Ваши расходы", size=33)
    name_input = ft.TextField(label="Название расхода")
    amount_input = ft.TextField(label="Сумма расхода")
    add_button = ft.ElevatedButton("Добавить", on_click=add_expense)

    expense_count_text = ft.Text(
        value=f"Общая сумма расходов: {db.total_expenses()} сом",
        size=28,
        color=ft.colors.PINK
    )

    expense_list_area = ft.Column(
        controls=get_rows(),
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    form_area = ft.Row(controls=[name_input, amount_input, add_button])

    page.add(title, form_area, expense_count_text, expense_list_area)

ft.app(main)