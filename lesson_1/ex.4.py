def to_out_bytes(word):
    enc_str_bytes = word.encode('utf-8')
    print(f'байтовое представление слова "{word}": {enc_str_bytes}')

    dec_str_bytes = enc_str_bytes.decode('utf-8')
    print(f'декодирование: {dec_str_bytes}')

word1 = 'разработка'
word2 = 'класс'
word3 = 'protocol'
word4 = 'standard'

to_out_bytes(word1)
to_out_bytes(word2)
to_out_bytes(word3)
to_out_bytes(word4)