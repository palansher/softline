from university_models import University, Faculty, Student

def run_demo() -> None:
    # Создание универа и факультетов
    my_uni = University("МГТУ им. Баумана")

    fac_it = Faculty("Информатика")
    fac_robotics = Faculty("Робототехника")

    my_uni.add_faculty(fac_it)
    my_uni.add_faculty(fac_robotics)

    # Создание 3 студентов
    student1 = Student("Иванов И.И.", fac_it)
    student2 = Student("Петров П.П.", fac_it)
    student3 = Student("Сидоров С.С.", fac_robotics)

    print(f"--- Университет: {my_uni.university_name} ---")

    # Демонстрация get_faculty_by_name
    faculty_search_name = "Информатика"
    found_faculty = my_uni.get_faculty_by_name(faculty_search_name)

    if found_faculty:
        print(f"\nНайден факультет: {found_faculty.faculty_name}")

        # Демонстрация get_student_by_id внутри найденного факультета
        search_id = 1002
        found_student = found_faculty.get_student_by_id(search_id)

        if found_student:
            print(f"На факультете найден студент по ID {search_id}:")
            print(f" > {found_student.get_student_info()}")
        else:
            print(f"Студент с ID {search_id} на факультете {faculty_search_name} не найден.")
    else:
        print(f"Факультет {faculty_search_name} не существует.")

    print("\nОбщий список студентов университета до перевода:")
    my_uni.print_all_students()

    # Демонстрация ошибочного перевода в тот же факультет
    print("\n--- Процесс ошибочного перевода в тот же факультет ---")
    student3.transfer_to(fac_robotics)

    # Демонстрация корректного перевода
    print("\n--- Процесс корректного перевода ---")
    student3.transfer_to(fac_it)

    print("\nОбщий список студентов университета после перевода:")
    my_uni.print_all_students()

"""
Когда запускаем файл напрямую, его скрытая переменная __name__ принимает значение "__main__".
Если же мы импортируем этот файл в другой (как мы сделали в main.py), то код внутри этого блока не выполнится.
Для чего это нужно:
Чтобы мы могли протестировать функционал прямо в файле с классами, но при импорте этих классов в основной проект функции "не запускались".
"""
if __name__ == "__main__":
    run_demo()
