# Задание 3.
word_one = b'attribute'
# word_two = b'класс'    -> SyntaxError: bytes can only contain ASCII literal characters
#                           а кирилицы в ASCII нет
# word_tree = b'функция' -> SyntaxError: bytes can only contain ASCII literal characters
word_fore = b'type'
print(word_one, type(word_one), len(word_one))
# print(word_two, type(word_two), len(word_two))
# print(word_tree, type(word_tree), len(word_tree))
print(word_fore, type(word_fore), len(word_fore))
