import tkinter as tk
from tkinter import ttk

from app.utils.database import Database

def create_user_list():
    # Создание виджета Treeview
    db = Database()
    users = db.read()
    tree = ttk.Treeview(window, columns=("username", "blocking", "password_limit"), show="headings")

    # Настройка заголовков столбцов
    tree.heading("username", text="Имя пользователя")
    tree.heading("blocking", text="Блокировка учетной записи")
    tree.heading("password_limit", text="Ограничения на пароль")

    # Установка размеров столбцов
    tree.column("username", width=250)
    tree.column("blocking", width=250)  
    tree.column("password_limit", width=250)

  

    # Вставка данных пользователей в список
    for i, user in enumerate(users.values()):
        tree.insert("", tk.END, values=(user.username, not user.active, user.restrictions))

    # Создание обработчика клика на строки
    def on_click(event):
        row = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if row:
            # Получение индекса строки
            name = tree.item(row)['values'][0]
            column_name = tree['columns'][int(col[1:]) - 1]
            # Изменение состояния флагов

            if column_name == 'password_limit':
                users[name].restrictions = not users[name].restrictions
                db.change_restriction_user(username=name, restrictions=users[name].restrictions)
            elif column_name == 'blocking':
                users[name].active = not users[name].active
                db.change_active_user(username=name, active=users[name].active)
            

            # Обновление данных в Treeview
            tree.item(row, values=(users[name].username, not users[name].active, users[name].restrictions))

    tree.bind("<Button-1>", on_click)

    return tree

def open_window():

    # Создание основного окна
    global window
    window = tk.Tk()
    window.title("Ограничения пользователей")
    window.geometry("850x300+800+300")

    # Создание списка пользователей
    user_list = create_user_list()
    user_list.pack()

    close_btn = ttk.Button(window, text='Закрыть окно', command=window.destroy)
    close_btn.place(x=350, y=250, width=150)


    # Запуск цикла обработки событий
    window.mainloop()
