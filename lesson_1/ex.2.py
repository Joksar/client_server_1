def to_bytes(word):
    x = eval('b"'+f'{word}"')
    print(f'{x}, {type(x)}, length = {len(x)}')

word1 = 'class'
word2 = 'function'
word3 = 'method'

to_bytes(word1)
to_bytes(word2)
to_bytes(word3)

