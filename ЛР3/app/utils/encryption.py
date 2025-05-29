import string

# def form_alphabet():
#     english_symbols = string.printable
#     russian_symbols = (''.join([chr(i) for i in range(ord('а'), ord('я') + 1)]) 
#                        + ''.join([chr(i) for i in range(ord('А'), ord('Я') + 1)]))
#     alphabet =russian_symbols + english_symbols[:-4]
#     return alphabet

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

    if len(key) > len(login):
        key = key[0:len(login)]
    
    while len(login) % len(key) != 0:
        login +=' '
    
    blocks = []
    while login :
        blocks.append(login[0:len(key)])
        login = login[len(key): len(login)]

    # Перестановка
    c = []
    for block in blocks:
        for j in range(len(key)):
            c.append(block[key[j]])

    return ''.join([str(c_i) for c_i in c])

def gamming(message, password):
    a = ord(password[0])
    c = ord(password[1])
    g0 = ord(password[3])

    cryptotext = []
    for i in range(len(message)):
        cryptotext.append(chr(g0 ^ ord(message[i])))
        g0 = (g0 * a + c) % 256
    return ''.join([str(el) for el in cryptotext])

def coding(login, password):

    hash_password_part_1 = rearrangement(login, password)
    hash_password_part_2 = gamming(hash_password_part_1, password)
    return hash_password_part_2


# print(coding('admin', 'Aa1+'))