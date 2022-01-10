import json

def write_order_to_json(dict):
    with open('orders.json', 'w', encoding='utf-8') as f_n:
        json.dump(dict, f_n, indent=4, ensure_ascii=False)


dict = {
    'Товар':'Lego 75295',
    'Количество': 135,
    'Buyer': 'Ricardo Milos',
    'Дата': '23.12.2021'
}

write_order_to_json(dict)