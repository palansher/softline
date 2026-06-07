"""Построим 10 домов"""

from random import randint, choice

# Варианты фундаментов
base_kinds = ['ленточный','сваи','плиты']
box_kinds = ['кирпич','дерево','блоки']
roof_kinds = ['шифер','металлочерепица']

def build_base(type):
    print(f"Фундамент {type} построен")

def build_box(type):
    print(f"Коробка из материала: {type} построена")


def build_roof(type):
    print(f"Крыша из материала: {type} построена")

def build_house(fundament,roof,box,address):
    build_base(fundament)
    build_box(box)
    build_roof(roof)
    print("Дом по адресу",address,"построен!")

STREET = "Пионерская"
for i in range(1,11):
    address = f"{STREET} {randint(1,100)}"
    print(f"Строим дом №{i} по адресу: {address}")
    build_house(choice(base_kinds),choice(roof_kinds),choice(box_kinds),address)
    print("*"*50)