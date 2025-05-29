import tkinter as tk
from tkinter import ttk

from app.utils.database import Database

def create_user_list(users: dict):
    # Создание виджета Treeview
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
    for user in users.values():
        tree.insert("", tk.END, values=(user.username, not user.active, user.restrictions))

    return tree

def open_window():
    global window
    db = Database()

    window = tk.Tk()
    window.title("Список пользователей")
    window.geometry("850x300+800+300")

    # Создание списка пользователей
    user_list = create_user_list(users=db.read())
    user_list.pack()

    close_btn = ttk.Button(window, text='Закрыть окно', command=window.destroy)
    close_btn.place(x=350, y=250, width=150)
