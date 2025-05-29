import tkinter as tk
from tkinter import ttk

from app.utils.database import Database, User

def open_window():

    # Создание окна
    window = tk.Tk()
    window.title("Добавление нового пользователя")
    window.geometry("300x200+800+300")

    # Надписи
    username_label = ttk.Label(window, text="Логин нового пользователя:")

    # Поля ввода
    global username_entry
    global result_label
    username_entry = ttk.Entry(window)

    # Кнопки
    login_button = ttk.Button(window, text="Добавить", command=add_new_user)
    exit_button = ttk.Button(window, text="Отмена", command=window.destroy)

    # Текст результата
    result_label = ttk.Label(window, text="")

    # Размещение элементов
    username_label.place(x=20, y=20, width=250)
    username_entry.place(x=20, y=70, width=250)

    login_button.place(x=50, y=120, width=80)
    exit_button.place(x=170, y=120, width=80)

    result_label.place(x=60, y=160, width=250)

def add_new_user():
    try:
        username = username_entry.get().lower()
        db = Database()
        user = User(username=username, password='')
        db.add_user(user)
        result_label['text'] = f'Вы добавили пользователя \nс именем {username}'

    except Exception as e:
        result_label['text'] = 'Пользователь с таким \nименем уже существует'
