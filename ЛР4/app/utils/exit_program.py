import os

from app.utils.encryption import encrypt_file


def close_program(window):
    from app.GUI.secret_phrase import key

    encrypt_file(key, 'temp_database.txt', 'database.txt')
    os.remove('temp_database.txt')
    window.destroy()
