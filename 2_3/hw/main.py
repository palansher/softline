from accounting import CarNumberSystem

def main():
    """
    Взаимодействие с пользователем.
    """
    car_accounting = CarNumberSystem()
    
    print("--- Система учета транспорта ---")
    region = input("Введите регион для регистрации: ").strip()

    # Заполняем 5 записей: водитель - номер
    for i in range(1, 6):
        print(f"\nРегистрация владельца №{i}")
        owner_name_input = input("Введите ФИО владельца: ")
     
        car_number = car_accounting.register_new_entry(owner_name_input, region)
        print(f"Успешно! Для {owner_name_input} закреплен номер: {car_number}")

    # Итоговый вывод
    car_accounting.display_all()

    # Поиск
    number_search_query = input("\nВведите номер для поиска владельца: ").strip()
    car_owner = car_accounting.find_owner(number_search_query)
    
    if car_owner:
        print(f"Владелец: {car_owner}")
    else:
        print("Запись не найдена.")

if __name__ == "__main__":
    main()
