# Задание 3.
word_list = ['attribute', 'класс', 'функция', 'type']
for word in word_list:
    try:
        print(bytes(word, 'ascii'))
    except UnicodeEncodeError as error:
        print(
            f'Невозможно преобразовать "{word}" в байты, сообщение ошибки:\n {error}')
