# Задание 4.
word_list = ['разработка', 'администрирование', 'protocol', 'standart']
for word in word_list:
    print(word, type(word))
    word = word.encode('utf-8')
    print(word, type(word))
    word = word.decode('utf-8')
    print(word, type(word))
