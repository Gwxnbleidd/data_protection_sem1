import tkinter as tk
from tkinter import ttk

from app.GUI.change_password_window import open_window as open_change_pwd_window
from app.GUI.users_list_window import open_window as open_users_list_window
from app.GUI.add_user_window import open_window as open_add_user_window
from app.GUI.limits_window import open_window as open_limits_window
from app.utils.database import Database

db = Database()

def is_admin(func):

    def decorator(*args, **kwargs):
        user = current_user
        if user == 'admin':
            res_label['text'] = ""
            return func(*args, **kwargs)
        else:
            res_label['text'] = "Только админ может это выполнить"
    return decorator

# Переопределяем функции для избежания цикличного вызова
@is_admin
def my_open_add_user_window():
    open_add_user_window()

@is_admin
def my_open_users_list_window():
    open_users_list_window()

@is_admin
def my_open_limits_window():
    open_limits_window()

# --- Основное окно ---
def open_main_window():
    global main_window
    main_window = tk.Tk()
    main_window.title("Главное окно")
    main_window.geometry("300x310+800+300")

    # --- Кнопки ---

    change_password_button = ttk.Button(main_window, text="Сменить пароль", command=open_change_pwd_window)
    show_users_button = ttk.Button(main_window, text="Просмотреть список пользователей", command=my_open_users_list_window)
    add_user_button = ttk.Button(main_window, text="Добавить пользователя", command=my_open_add_user_window)
    block_user_button = ttk.Button(main_window, text="Блокировка / Ограничения", command=my_open_limits_window)
    change_user = ttk.Button(main_window, text="Сменить пользователя", command=exit_window_and_login_window)
    exit_button = ttk.Button(main_window, text="Выйти", command=exit)
    global res_label
    res_label = ttk.Label(main_window, text='')

    change_password_button.place(x=15, y=20, width=270)
    show_users_button.place(x=15, y=60, width=270)
    add_user_button.place(x=15, y=100, width=270)
    block_user_button.place(x=15, y=140, width=270)
    change_user.place(x=15, y=180, width=270)
    exit_button.place(x=15, y=220, width=270)
    res_label.place(x=15, y=260, width=270)

    menubar = tk.Menu(main_window)

    # Создание пункта меню "Справка"
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="О программе", command=show_about)
    menubar.add_cascade(label="Справка", menu=helpmenu)

    # Установка меню в главное окно
    main_window.config(menu=menubar)

def login_attempts(func):
    count = 0

    def decorator(*args, **kwagrs):
        nonlocal count
        res = func(*args, **kwagrs)
        if not res:
            count += 1
            if count == 3:
                exit()
            result_label['text'] = f"Неверный логин или пароль\nОсталось попыток: {3-count}!"
        else:
            count = 0
            return res
    return decorator

@login_attempts
def login(name: int, pwd: int, database):
    
    user = database.find_user(name)

    if user.password == pwd:
        return True
    return False

def login_clk():
    username = username_entry.get().lower()
    pwd = password_entry.get()
    try:
        global current_user
        current_user = db.find_user(username)
        if current_user.active:
            if current_user.password == "":
                current_user = current_user.username
                open_change_pwd_window()
            else:
                if login(username, pwd, db):
                    current_user = current_user.username
                    window.destroy()
                    open_main_window()
        else:
            result_label['text'] = 'Пользователь заблокирован'
            return False
    except Exception as e:
        result_label['text'] = e.args[0]

def login_window(arg = None):
    # Создание окна
    global window
    window = tk.Tk()
    window.title("Авторизация")
    window.geometry("300x200+800+300")

    # Надписи
    username_label = ttk.Label(window, text="Логин:")
    password_label = ttk.Label(window, text="Пароль:")

    # Поля ввода
    global username_entry
    global password_entry
    username_entry = ttk.Entry(window)
    password_entry = ttk.Entry(window, show="*")

    # Кнопки
    login_button = ttk.Button(window, text="Войти", command=login_clk)
    exit_button = ttk.Button(window, text="Выйти", command=exit)

    # Текст результата
    global result_label
    result_label = ttk.Label(window, text="")

    # Размещение элементов
    username_label.place(x=20, y=20)
    username_entry.place(x=100, y=20, width=150)

    password_label.place(x=20, y=60)
    password_entry.place(x=100, y=60, width=150)

    login_button.place(x=50, y=120, width=80)
    exit_button.place(x=170, y=120, width=80)

    result_label.place(x=60, y=160, width=250)

    if arg == 'mainloop':
        window.mainloop()

def exit_window_and_login_window():
    main_window.destroy()
    login_window()

def show_about():
    about_window = tk.Toplevel(main_window)
    about_window.title("О программе")
    about_window.geometry("330x200+800+300")
    
    label = tk.Label(about_window, text="А-13-21 \nГайчуков Дмитрий \nВ29 \nНаличие строчных и прописных букв, \nцифр и знаков арифметических операций.")
    label.place(x=10, y=10, width=320, height=120)

    button = tk.Button(about_window, text="Закрыть", command=about_window.destroy)
    button.place(x=100 ,y=150, width=100)
