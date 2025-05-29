import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json

from app.utils.database import Database


def form_key(password: str):
    key = []
    password = list(password)
    sort_password = sorted(password)
    for el in password:
        index = sort_password.index(el)
        key.append(index)
        sort_password[index] = '\1'
    return key


def rearrangement(login, password):
    # Формирование ключа
    key = form_key(password)

    while len(login) % len(key) != 0:
        login += ' '

    blocks = []
    while login:
        blocks.append(login[0:len(key)])
        login = login[len(key): len(login)]

    # Перестановка
    c = []
    for block in blocks:
        for j in range(len(block)):
            c.append(block[key[j]])

    return ''.join([str(c_i) for c_i in c])


def gamming(message, password):
    a = ord(password[0])
    c = ord(password[1])
    g0 = ord(password[2])

    cryptotext = []
    for i in range(len(message)):
        cryptotext.append(chr(g0 ^ ord(message[i])))
        g0 = (g0 * a + c) % 256
    return ''.join([str(el) for el in cryptotext])


def coding(login, password):
    if len(password) > len(login):
        password = password[0:len(login)]

    hash_password_part_1 = rearrangement(login, password)
    hash_password_part_2 = gamming(hash_password_part_1, password)
    return hash_password_part_2


def generate_key_using_phrase(phrase, salt):
    return hashlib.pbkdf2_hmac('sha256', phrase.encode(), salt, 100000)


# Шифрование данных
def encrypt_data(key, plaintext):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

    # Возвращаем вектор и зашифрованные данные
    return cipher.iv + ciphertext


# Расшифровка данных
def decrypt_data(key, ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size).decode()


# Хеширование данных с использованием SHA-256
def calculate_hash(data):
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def encrypt_file(key, file, crypt_file):
    db = Database(file)
    data = db.read()

    # Преобразуем словарь в строку JSON
    json_data = json.dumps(data)

    crypt_data = encrypt_data(key, json_data)
    with open(crypt_file, 'wb+') as file:
        file.write(crypt_data)


def form_decrypt_file(key):
    with open('database.txt', 'rb+') as file:
        crypt_data = file.read()

    text = decrypt_data(key, crypt_data)

    # Загружаем данные из JSON-строки
    data = json.loads(text)

    with open('temp_database.txt', 'w') as file:
        # Преобразуем словарь в строку JSON
        json_data = json.dumps(data, indent=4)
        file.write(json_data)
