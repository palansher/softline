from pprint import pprint

abonents = [
    {
        'Иванов': ['+7960242423', '+7960242420']
    },
    {
        'Петров': ['+7960242421', '+7960242422', '+7960242412']
    },
    {
        'Сидоров': ['+7960242121']
    }
]

# pprint(abonents)

for i,abonent in enumerate(abonents,1):
    for fio,phones in abonent.items():
        if phones:
            if len(phones)>1:
                print(f'{i}) Абонент {fio} имеет телефоны {", ".join(phones)}')
            else:
                print(f'{i}) Абонент {fio} имеет телефон {phones[0]}')