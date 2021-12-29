import chardet
import re
import csv


def get_data():
    os_name_list = []
    prod_code_list = []
    sys_manuf = []
    sys_type = []
    main_data = []

    for i in range(3):

        with open(f'info_{i+1}.txt', 'rb') as f:
            content = f.read()
            encoding = chardet.detect(content)['encoding']
        f.close()

        with open(f'info_{i+1}.txt', encoding=encoding) as f:
            for string in f:
                a = re.search('Наз.*|Изготовитель с.*|Код.*|Тип.*', string)
                if a:
                    a = re.sub(':   *', '---', string)
                    a = re.sub('\n', '', a)
                    a = re.split('---', a, maxsplit=0)
                    main_data.append(a[0])
                    if 'Название ОС' in a[0]:
                        os_name_list.append(a[1])
                    elif 'Изготовитель системы' in a[0]:
                        sys_manuf.append(a[1])
                    elif 'Код' in a[0]:
                        prod_code_list.append(a[1])
                    elif 'Тип' in a[0]:
                        sys_type.append(a[1])
    main_data = [main_data[0:4]]
    for i in range(len(os_name_list)):
        main_data.append([os_name_list[i]])
        main_data[i+1].append(prod_code_list[i])
        main_data[i+1].append(sys_manuf[i])
        main_data[i+1].append(sys_type[i])
    # print(os_name_list)
    # print(sys_manuf)
    # print(prod_code_list)
    # print(sys_type)
    # print(main_data)
    return main_data


print(get_data())

def write_to_csv():
    with open ('ex_1.csv', 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in get_data():
            f_n_writer.writerow(row)

write_to_csv()
