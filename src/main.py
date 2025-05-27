import flet as ft

from database import Database


def main(page: ft.Page):
    page.title = "Приложение для учёта расходов"
    page.window_width = 1024
    page.data = 0

    db = Database("db.sqlite3")
    db.create_tables()

    def get_rows() -> list[ft.Row]:
        rows = []
        for expense in db.all_expenses():
            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(value=str(expense[0]), size=30),
                        ft.Text(value=f"Расход: {expense[1]}", size=30),
                        ft.Text(
                            value=f"Сумма: {expense[2]} сом",
                            size=30,
                            color=ft.Colors.BLUE,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT_NOTE,
                            icon_color=ft.Colors.GREEN,
                            icon_size=20,
                            on_click=open_edit_modal,
                            data=expense[0],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
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

        name_input.value = ""
        amount_input.value = ""

        expense_list_area.controls = get_rows()
        expense_total_text.value = f"Общая сумма: {db.total_expenses()} сом"

        page.update()

    def delete_expense(e):
        print(f"Удаляем расход с id={e.control.data}")

        db.delete_expense_by_id(expense_id=e.control.data)

        expense_list_area.controls = get_rows()
        expense_total_text.value = f"Общая сумма: {db.total_expenses()} сом"
        page.update()

    def open_edit_modal(e):
        page.data = e.control.data
        expense = db.get_expense_by_id(expense_id=page.data)
        name_input.value = expense[1]
        amount_input.value = str(expense[2])
        page.open(edit_modal)

    def close_edit_modal(e):
        page.close(edit_modal)

    def update_expense(e):
        db.update_expense(
            expense_id=page.data,
            name=name_input.value,
            amount=amount_input.value,
        )
        expense_list_area.controls = get_rows()
        page.close(edit_modal)
        name_input.value = ""
        amount_input.value = ""
        expense_total_text.value = f"Общая сумма: {db.total_expenses()} сом"
        page.update()

    title = ft.Text(value="Учёт расходов", size=33)
    name_input = ft.TextField(label="Название расхода")
    amount_input = ft.TextField(label="Сумма расхода")
    add_button = ft.ElevatedButton("Добавить", on_click=add_expense)
    expense_total_text = ft.Text(
        value=f"Общая сумма: {db.total_expenses()} сом", size=28, color=ft.Colors.PINK
    )
    expense_list_area = ft.Column(controls=get_rows(), scroll="auto", expand=True)
    form_area = ft.Row(controls=[name_input, amount_input, add_button])
    title.value = "Ваши расходы"

    edit_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Редактировать расход"),
        content=ft.Column(
            controls=[
                name_input,
                amount_input,
            ]
        ),
        actions=[
            ft.ElevatedButton(
                "Сохранить",
                on_click=update_expense,
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
            ),
            ft.ElevatedButton("Отменить", on_click=close_edit_modal),
        ],
    )

    page.add(
        title,
        form_area,
        expense_total_text,
        expense_list_area,
    )


ft.app(main)