import flet as ft


import flet as ft
from database import Database

def main(page: ft.Page):
    page.title = "Управление контактами"
    page.window.width = 1200
    page.window.height = 700
    
    # Создаем экземпляр базы данных
    db = Database("contacts.sqlite3")
    db.create_tables()
    
    # Текст для отображения ошибок
    error_text = ft.Text(value="", color="red", size=14)
    success_text = ft.Text(value="", color="green", size=14)
    
    def clear_messages():
        """Очистка сообщений об ошибках и успехе"""
        error_text.value = ""
        success_text.value = ""
    
    def get_contact_rows():
        """
        Функция возвращает список Row с контактами для отображения в таблице
        """
        contacts = db.all_contacts()
        if not contacts:
            return [ft.Row([ft.Text("Контакты не найдены", size=16, color="gray")])]
        
        rows = []
        # Заголовок таблицы
        rows.append(
            ft.Row(
                controls=[
                    ft.Text("ID", size=14, weight=ft.FontWeight.BOLD, width=50),
                    ft.Text("Имя", size=14, weight=ft.FontWeight.BOLD, width=200),
                    ft.Text("Телефон", size=14, weight=ft.FontWeight.BOLD, width=150),
                    ft.Text("Примечание", size=14, weight=ft.FontWeight.BOLD, width=250),
                    ft.Text("Действия", size=14, weight=ft.FontWeight.BOLD, width=100),
                ],
                spacing=10
            )
        )
        
        # Разделитель
        rows.append(ft.Divider())
        
        # Строки с контактами
        for contact in contacts:
            contact_id, name, phone, note = contact
            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(str(contact_id), size=14, width=50),
                        ft.Text(name, size=14, width=200),
                        ft.Text(phone, size=14, width=150),
                        ft.Text(note or "-", size=14, width=250),
                        ft.ElevatedButton(
                            "Удалить",
                            on_click=delete_contact,
                            data=contact_id,
                            color="white",
                            bgcolor="red",
                            width=80
                        ),
                    ],
                    spacing=10
                )
            )
        
        return rows
    
    def add_contact(e):
        """
        Функция добавления нового контакта
        """
        clear_messages()
        
        # Проверяем заполненность обязательных полей
        if not name_input.value.strip():
            error_text.value = "Ошибка: Имя контакта не может быть пустым!"
            page.update()
            return
        
        if not phone_input.value.strip():
            error_text.value = "Ошибка: Номер телефона не может быть пустым!"
            page.update()
            return
        
        try:
            # Добавляем контакт в базу данных
            db.add_contact(
                name=name_input.value.strip(),
                phone=phone_input.value.strip(),
                note=note_input.value.strip()
            )
            
            # Обновляем список контактов
            contacts_area.controls = get_contact_rows()
            
            # Обновляем счетчик контактов
            contact_count_text.value = f"Всего контактов: {db.count_contacts()}"
            
            # Очищаем поля ввода
            name_input.value = ""
            phone_input.value = ""
            note_input.value = ""
            
            # Показываем сообщение об успехе
            success_text.value = "Контакт успешно добавлен!"
            
            page.update()
            
        except Exception as ex:
            error_text.value = f"Ошибка при добавлении контакта: {str(ex)}"
            page.update()
    
    def delete_contact(e):
        """
        Функция удаления контакта
        """
        clear_messages()
        
        try:
            contact_id = e.control.data
            db.delete_contact(contact_id)
            
            # Обновляем список контактов
            contacts_area.controls = get_contact_rows()
            
            # Обновляем счетчик контактов
            contact_count_text.value = f"Всего контактов: {db.count_contacts()}"
            
            success_text.value = "Контакт успешно удален!"
            page.update()
            
        except Exception as ex:
            error_text.value = f"Ошибка при удалении контакта: {str(ex)}"
            page.update()
    
    # Создаем элементы интерфейса
    title = ft.Text("Управление контактами", size=32, weight=ft.FontWeight.BOLD)
    
    # Поля ввода
    name_input = ft.TextField(
        label="Имя контакта *",
        hint_text="Введите имя контакта",
        width=250
    )
    
    phone_input = ft.TextField(
        label="Номер телефона *",
        hint_text="Введите номер телефона",
        width=200
    )
    
    note_input = ft.TextField(
        label="Примечание",
        hint_text="Дополнительная информация (необязательно)",
        width=300
    )
    
    # Кнопка добавления
    add_button = ft.ElevatedButton(
        "Добавить контакт",
        on_click=add_contact,
        bgcolor=ft.colors.BLUE,
        color="white",
        width=150
    )
    
    # Счетчик контактов
    contact_count_text = ft.Text(
        f"Всего контактов: {db.count_contacts()}",
        size=18,
        weight=ft.FontWeight.BOLD
    )
    
    # Область для отображения контактов
    contacts_area = ft.Column(
        controls=get_contact_rows(),
        spacing=5,
        scroll=ft.ScrollMode.AUTO,
        height=400
    )
    
    # Форма для добавления контакта
    form_area = ft.Row(
        controls=[name_input, phone_input, note_input, add_button],
        spacing=15,
        alignment=ft.MainAxisAlignment.START
    )
    
    # Контейнер для таблицы контактов
    contacts_container = ft.Container(
        content=contacts_area,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=8,
        padding=10,
        bgcolor=ft.colors.GREY_50
    )
    
    # Добавляем все элементы на страницу
    page.add(
        title,
        ft.Text("* - обязательные поля", size=12, color="gray"),
        form_area,
        error_text,
        success_text,
        ft.Divider(),
        contact_count_text,
        contacts_container
    )


ft.app(main)




import sqlite3

class Database:
    def __init__(self, db_path: str):
        """
        Инициализация класса Database
        
        Args:
            db_path (str): Путь к файлу базы данных SQLite
        """
        self.db_path = db_path
    
    def create_tables(self):
        """Создает таблицу контактов если она не существует"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                note TEXT DEFAULT ''
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_contact(self, name: str, phone: str, note: str = ""):
        """
        Добавляет новый контакт в базу данных
        
        Args:
            name (str): Имя контакта
            phone (str): Номер телефона
            note (str): Дополнительная пометка (по умолчанию пустая)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contacts (name, phone, note) 
            VALUES (?, ?, ?)
        ''', (name, phone, note))
        
        conn.commit()
        conn.close()
    
    def delete_contact(self, contact_id: int):
        """
        Удаляет контакт по ID
        
        Args:
            contact_id (int): ID контакта для удаления
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        
        conn.commit()
        conn.close()
    
    def all_contacts(self):
        """
        Возвращает список всех контактов из базы данных
        
        Returns:
            list: Список кортежей (id, name, phone, note)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, phone, note FROM contacts ORDER BY name')
        contacts = cursor.fetchall()
        
        conn.close()
        return contacts
    
    def get_contact_by_id(self, contact_id: int):
        """
        Получает контакт по ID (дополнительный метод для расширения функциональности)
        
        Args:
            contact_id (int): ID контакта
            
        Returns:
            tuple: Кортеж (id, name, phone, note) или None если контакт не найден
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, phone, note FROM contacts WHERE id = ?', (contact_id,))
        contact = cursor.fetchone()
        
        conn.close()
        return contact
    
    def update_contact(self, contact_id: int, name: str, phone: str, note: str = ""):
        """
        Обновляет существующий контакт (дополнительный метод для расширения функциональности)
        
        Args:
            contact_id (int): ID контакта для обновления
            name (str): Новое имя контакта
            phone (str): Новый номер телефона
            note (str): Новая пометка
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE contacts 
            SET name = ?, phone = ?, note = ? 
            WHERE id = ?
        ''', (name, phone, note, contact_id))
        
        conn.commit()
        conn.close()
    
    def search_contacts(self, search_term: str):
        """
        Поиск контактов по имени или номеру телефона (дополнительный метод)
        
        Args:
            search_term (str): Строка для поиска
            
        Returns:
            list: Список найденных контактов
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, note FROM contacts 
            WHERE name LIKE ? OR phone LIKE ? 
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        contacts = cursor.fetchall()
        
        conn.close()
        return contacts
    



    import flet as ft from database import Database  def main(page: ft.Page):     page.title = "Менеджер контактов"     page.window_width = 1024     page.data = 0  # id контакта      db = Database("contacts.sqlite3")     db.create_tables()     contacts = db.all_contacts()     print(contacts)      def get_rows() -> list[ft.Row]:         rows = []         for contact in db.all_contacts():             rows.append(                 ft.Row(                     controls=[                         ft.Text(f"{contact[1]} | {contact[2]} | {contact[3]}", expand=True),                         ft.IconButton(icon=ft.icons.DELETE, on_click=delete_contact, data=contact[0]),                     ]                 )             )         return rows      def add_contact(e):         db.add_contact(name=name_input.value, phone=phone_input.value, note=note_input.value)         contact_list.controls = get_rows()         name_input.value = ""         phone_input.value = ""         note_input.value = ""         page.update()      def delete_contact(e):         db.delete_contact(contact_id=e.control.data)         contact_list.controls = get_rows()         page.update()      title = ft.Text(value="Контакты", size=33)     name_input = ft.TextField(label="Имя контакта")     phone_input = ft.TextField(label="Телефон")     note_input = ft.TextField(label="Примечание")      add_button = ft.ElevatedButton(text="Добавить", on_click=add_contact)     form_area = ft.Row(controls=[name_input, phone_input, note_input, add_button])      contact_list = ft.Column(controls=get_rows(), scroll=ft.ScrollMode.AUTO)      page.add(title, form_area, contact_list)  ft.app(main) в чем ошибка если задание Создать небольшое приложение на Flet для управления списком контактов(как на телефоне), с сохранением данных в базе данных.
Что должно быть в приложении:
* Текстовые поля:
   * Имя контакта
   * Номер телефона
   * Дополнительная пометка(может быть пустой)
* Кнопка "Добавить":
При нажатии новый контакт сохраняется в базу данных.
* Таблица ниже формы:
   * Отображает все контакты из базы данных.
   * У каждого контакта должна быть кнопка "Удалить" для его удаления из БД. Удаление можно сделать без AlertDialog
Работа с базой данных:
* Использовать отдельный класс Database для работы с БД(в отдельном файле):
   * Метод для создания таблицы контактов.
   * Метод для добавления контакта.
   * Метод для удаления контакта.
   * Метод для получения списка всех контактов.
Что будет храниться в БД:
Каждый контакт должен содержать:
* ID (целое число, уникальный идентификатор, автоинкремент)
* Имя контакта(строка)
* Номер(строка!)
* Дополнительная пометка(строка)

Код выглядит правильным и должен работать согласно вашему заданию. Однако есть несколько потенциальных проблем, которые могут вызывать ошибки:

Возможные причины ошибок:
1. Отсутствует файл database.py
Самая вероятная причина - отсутствует файл с классом Database. Вот как он должен выглядеть:


database.py
Code 
2. Улучшения основного кода
Ваш основной код можно улучшить, добавив проверки на пустые поля:


main.py (улучшенная версия)
Code 
Основные исправления:
Создан класс Database с необходимыми методами
Добавлена валидация - проверка на пустые обязательные поля
Улучшен интерфейс - добавлены уведомления об ошибках
Оптимизирован код - убрана неиспользуемая переменная page.data
Структура файлов:
project/
├── main.py          # основной файл приложения
├── database.py      # класс для работы с БД
└── contacts.sqlite3 # файл базы данных (создается автоматически)
Убедитесь, что у вас установлен Flet:

bash
pip install flet
Теперь приложение должно работать правильно и соответствовать всем требованиям задания!





создай файл для database


database.py
Code 
Вот готовый файл database.py с классом Database. Класс содержит все необходимые методы согласно заданию:

Основные методы (требуемые по заданию):
create_tables() - создание таблицы контактов
add_contact() - добавление нового контакта
delete_contact() - удаление контакта по ID
all_contacts() - получение списка всех контактов
Дополнительные методы (для расширения функциональности):
get_contact_by_id() - получение конкретного контакта
update_contact() - обновление существующего контакта
search_contacts() - поиск контактов
Структура таблицы в БД:
id - INTEGER PRIMARY KEY AUTOINCREMENT (уникальный идентификатор)
name - TEXT NOT NULL (имя контакта)
phone - TEXT NOT NULL (номер телефона как строка)
note - TEXT DEFAULT '' (дополнительная пометка)
Сохраните этот код в файл database.py в той же папке, где находится ваш основной файл с приложением Flet. После этого ваше приложение должно работать корректно!




import sqlite3
# CRUD - Create, Read, Update, Delete
class Database:
    """
    Класс для работы с БД. тут будут методы для создания таблиц,
    для добавления, обновления и удаления задач(таблица todos)
    """
    def init(self, path):
        self.path = path
    def create_tables(self):
        """
        Метод, в котором описывается, какие таблицы и с какими колонками создаются для приложения
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    category TEXT
                )
            """)
    def count_todos(self):
        """
        Метод, в котором вызывается запрос для получения количества задач из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT COUNT(*) FROM todos")
            # (0)
            return result.fetchone()[0]
    def all_todos(self):
        """
        Метод, в котором вызывается запрос для получения всех задач из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM todos")
            return result.fetchall()
    def get_todo(self, todo_id):
        """
        Метод, в котором вызывается запрос для получения конкретной задачи из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM todos WHERE id=(?)", (todo_id,))
            # (1, 'cook meal', 'home')
            return result.fetchone()
    def add_todo(self, task: str, category: str):
        """
        Метод, в котором вызывается запрос для добавления в БД новой задачи
        """
        print(task, category, "in database add_todo")
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO todos (task, category) VALUES
                (?, ?)
                """,
                (task, category),
            )
            # так делать неправильно:
            # conn.execute(
            #     f"INSERT INTO todos (task, category) VALUES ({task}, {category})",
            # )
            conn.commit()
    def update_todo(self, todo_id: int, task: str, category: str):
        """
        Метод, в котором вызывается запрос для обновления задачи
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                UPDATE todos SET task = ?, category = ? WHERE
                id = ?
                """,
                (task, category, todo_id),
            )
    def delete_todo(self, todo_id):
        """
        Метод, в котором вызывается запрос для удаления задачи
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute("DELETE FROM todos WHERE id=(?)", (todo_id,)) создать код вот в такого примера только с нашими данными


database.py
Code 
Вот готовый файл database.py для работы с контактами, созданный по аналогии с вашим примером для todos:

Основные изменения по сравнению с примером:
Изменена таблица с todos на contacts
Поля таблицы: id, name, phone, note (вместо task, category)
Все методы адаптированы для работы с контактами
Добавлен параметр note со значением по умолчанию
Структура таблицы contacts:
id - INTEGER PRIMARY KEY AUTOINCREMENT (уникальный идентификатор)
name - TEXT NOT NULL (имя контакта)
phone - TEXT NOT NULL (номер телефона)
note - TEXT (дополнительная пометка, может быть пустой)
Доступные методы:
create_tables() - создание таблицы контактов
count_contacts() - подсчет количества контакт



import sqlite3

# CRUD - Create, Read, Update, Delete
class Database:
    """
    Класс для работы с БД. тут будут методы для создания таблиц,
    для добавления, обновления и удаления контактов(таблица contacts)
    """
    def __init__(self, path):
        self.path = path

    def create_tables(self):
        """
        Метод, в котором описывается, какие таблицы и с какими колонками создаются для приложения
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    note TEXT
                )
            """)

    def count_contacts(self):
        """
        Метод, в котором вызывается запрос для получения количества контактов из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT COUNT(*) FROM contacts")
            # (0)
            return result.fetchone()[0]

    def all_contacts(self):
        """
        Метод, в котором вызывается запрос для получения всех контактов из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM contacts")
            return result.fetchall()

    def get_contact(self, contact_id):
        """
        Метод, в котором вызывается запрос для получения конкретного контакта из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM contacts WHERE id=(?)", (contact_id,))
            # (1, 'Иван Иванов', '+7-123-456-78-90', 'Друг')
            return result.fetchone()

    def add_contact(self, name: str, phone: str, note: str = ""):
        """
        Метод, в котором вызывается запрос для добавления в БД нового контакта
        """
        print(name, phone, note, "in database add_contact")
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO contacts (name, phone, note) VALUES
                (?, ?, ?)
                """,
                (name, phone, note),
            )
            # так делать неправильно:
            # conn.execute(
            #     f"INSERT INTO contacts (name, phone, note) VALUES ({name}, {phone}, {note})",
            # )
            conn.commit()

    def update_contact(self, contact_id: int, name: str, phone: str, note: str = ""):
        """
        Метод, в котором вызывается запрос для обновления контакта
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                UPDATE contacts SET name = ?, phone = ?, note = ? WHERE
                id = ?
                """,
                (name, phone, note, contact_id),
            )
            conn.commit()

    def delete_contact(self, contact_id):
        """
        Метод, в котором вызывается запрос для удаления контакта
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute("DELETE FROM contacts WHERE id=(?)", (contact_id,))
            conn.commit()