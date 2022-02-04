import chardet
from chardet import detect

lines = ['сетевое программирование', 'сокет', 'декоратор' ]

f = open('test_file.txt', 'w', encoding='utf-8')
for i in lines:
    f.write(i+'\n')
f.close()

with open('test_file.txt', 'rb') as f:
    content = f.read()
    encoding = chardet.detect(content)['encoding']
    print(encoding)
f.close()

with open('test_file.txt', encoding=encoding) as f:
    for string in f:
        print(string)

