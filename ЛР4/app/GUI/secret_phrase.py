import time
import tkinter as tk
from tkinter import ttk
import os

from app.GUI.main_window import login_window
from app.utils.encryption import generate_key_using_phrase, form_decrypt_file, encrypt_file
from app.utils.database import User, Database


def open_window():
    # Создание окна
    global window
    window = tk.Tk()
    window.title("Ввод парольной фразы")
    window.geometry("300x200+800+300")

    # Надписи
    phrase_label = ttk.Label(window, text="Введите парольную фразу:")

    # Поля ввода
    global result_label
    global phrase_entry
    phrase_entry = ttk.Entry(window)

    # Кнопки
    confirm_button = ttk.Button(window, text="ОК", command=click_processing)
    exit_button = ttk.Button(window, text="Отмена", command=exit)

    # Текст результата
    result_label = ttk.Label(window, text="")

    # Размещение элементов
    phrase_label.place(x=20, y=20, width=250)
    phrase_entry.place(x=20, y=70, width=250)

    confirm_button.place(x=50, y=120, width=80)
    exit_button.place(x=170, y=120, width=80)

    result_label.place(x=60, y=160, width=250)

    window.mainloop()


def click_processing():
    # если файл не зашифрован - добавить пользователя и зашифровать
    # если зашифрован - расшифровать
    result_label['text'] = ''

    global key
    phrase = phrase_entry.get()

    if not os.path.exists('database.txt'):
        admin = User(username='admin', password='')
        database = Database('database.txt')
        database.add_user(admin)
        salt = os.urandom(16)
        with open('salt.txt', 'wb') as file:
            file.write(salt)
        key = generate_key_using_phrase(phrase, salt)
        encrypt_file(key, 'database.txt', 'database.txt')
    else:
        with open('salt.txt', 'rb') as file:
            salt = file.read()
        key = generate_key_using_phrase(phrase, salt)

    try:
        form_decrypt_file(key)
    except ValueError:
        result_label['text'] = 'Неверная парольная фраза'
        return

    db = Database()
    database = db.read()
    print(database)
    if database.get('admin'):
        window.destroy()
        login_window()
    else:
        result_label['text'] = 'Неверная парольная фраза'
        exit()
