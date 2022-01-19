def to_bytes(word):
    x = eval('b"'+f'{word}"')
    print(f'{x}, {type(x)}, length = {len(x)}')

word1 = 'attribute'
word2 = 'класс'
word3 = 'функция'
word4 = 'type'

to_bytes(word1)
#to_bytes(word2)
#to_bytes(word3)
to_bytes(word4)

"""
Знаки кириллицы не относятся к формату ASCII, и не могут быть представлены в байтовом виде.
"""