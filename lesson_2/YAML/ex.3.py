import yaml

key_1_data = ['Jack','John','Jason','Jeff']
key_2_data = 13
key_3_data = {
    'Ключ 1':'$',
    'Ключ 2':'§',
    'Ключ 3':'©'
}

data = {'key_1':key_1_data, 'key_2':key_2_data, 'key_3': key_3_data}

with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(data, f_n, default_flow_style=False, allow_unicode = True)

with open('file.yaml', encoding='utf-8') as f_n:
    print(f_n.read())