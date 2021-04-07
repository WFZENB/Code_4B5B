import random as rnd

dict_4b5b = {'0000': '11110', '0001': '01001', '0010': '10100', '0011': '10101',
             '0100': '01010', '0101': '01011', '0110': '01110', '0111': '01111',
             '1000': '10010', '1001': '10011', '1010': '10110', '1011': '10111',
             '1100': '11010', '1101': '11011', '1110': '11100', '1111': '11101'}
list_encode = []
list_send   = []
output      = ''


def hash(lst):
    check_sum = 0
    for b in lst:
        check_sum += int(b, 2)
    return check_sum % 255


# Кодирование сообщения
def encode(text):
    global output
    global list_encode
    list_encode = []

    # Разбиение сообщения на 4-битные последовательности
    # и их кодирование по таблице 4B/5B
    for lit in text:
        alpha_bin = format(ord(lit), '016b')
        bits = [alpha_bin[i:i + 4] for i in range(0, len(alpha_bin), 4)]
        for b in bits:
            list_encode.append(dict_4b5b[b])

    # Вычисление оригинального хеша
    orig_hash = hash(list_encode)
    output += ('Передатчик  | Исходный хеш    ' + str(orig_hash) + '\n\n')

    # Добавление хеша в конец передаваемого пакета
    hash_bin = format(orig_hash, '016b')
    hash_bits = [hash_bin[i:i + 4] for i in range(0, len(hash_bin), 4)]
    for b in hash_bits:
        list_encode.append(dict_4b5b[b])


# Отправка одной последовательности с возможной генерацией помех
def send_sequence(id):
    global output
    if rnd.randint(0, 100) == 0:

        # Передача последовательности с помехой
        noise = list('00000')
        noise[rnd.randint(0, 4)] = '1'
        list_send[id] = format(int(''.join(noise), 2) ^ int(list_encode[id], 2), '05b')
        output += ('Канал связи | Образовалась помеха \'' + ''.join(noise) +
                   '\' в последовательности ' + str(id) + '\n')

    else:

        # Передача последовательности без помех
        list_send[id] = list_encode[id]


# Отправка сообщения
def send_msg():
    global list_send
    list_send = [0] * len(list_encode)

    # Отправка всех последовательностей
    for i in range(len(list_encode)):
        send_sequence(i)


# Декодирование сообщения
def decode():
    global list_send
    global output

    # Извлечение огигинального хеша (4 последние последовательности)
    hash_bin = ''
    for i in range(4):
        hash_bin += list(dict_4b5b.keys())[list(dict_4b5b.values()).index(list_send[i + len(list_send)-4])]
    orig_hash = int(hash_bin, 2)
    output += ('Приемник    | Полученный хеш  ' + str(orig_hash) + '\n')
    list_send = list_send[:-4]

    # Вычисление хеша и выход из функции при несовпадении с оригиналльным хешем
    calc_hash = hash(list_send)
    output += ('Приемник    | Вычисленный хеш ' + str(calc_hash) + '\n')
    if orig_hash == calc_hash:
        output += 'Приемник    | Хеши равны\n'
    else:
        return False

    # Чтение, декодирование и возврат полученного сообщения
    received_msg = ''
    for i in range(0, len(list_send), 4):
        char = ''
        for j in range(4):
            char += list(dict_4b5b.keys())[list(dict_4b5b.values()).index(list_send[i + j])]
        received_msg += chr(int(char, 2))
    return received_msg


# Проверка на наличее помех в последовательности
def is_noise(id):
    return not list_send[id] in list(dict_4b5b.values())


# Получение сообщения
def get_msg():
    global output

    # Проверка каждой последовательности на наличее запрещенных
    # и повторная отправка этой последовательности пока не будет получена разрешенная
    for i in range(len(list_send)):
        while is_noise(i):
            output += ('Приемник    | Выявлена помеха в последовательности ' + str(i) + '. Повторный запрос\n')
            send_sequence(i)

    # Возврат декодированного сообщения
    return decode()


# Инициализатор отправки сообщения
def start_transfer(text):
    global output
    output = 'Передатчик  | Сообщение отправлено\n'
    encode(text)
    while True:
        send_msg()
        received_msg = get_msg()
        if received_msg:
            output += '\nПриемник    | Сообщение получено\n'
            return received_msg, output
        else:
            output += '\n> Контрольные суммы не сходятся! Повторная отправка сообщения\n\n'

