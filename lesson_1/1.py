# Задание 1.

word_list = ['разработка', 'сокет', 'декоратор']
for word in word_list:
    print(word, type(word), 'после преобразования:',
          word.encode('utf-8'), type(word.encode('utf-8')))

# строки в формате utf-8
unicode_list = [
    '\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0',
    '\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82',
    '\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80',
]
for word in unicode_list:
    print(word, type(word))

# строки в формате utf-16
unicode_list_16 = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440',
]

for word in unicode_list_16:
    print(word, type(word))
