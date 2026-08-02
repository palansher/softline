import random


from Passport import Passport


class PassportSystem:
    series = None
    list_numbers = [] #список паспортов
    def __init__(self,count_passports):
        """Заполнить коллекцию паспортами"""
        self.create_series()
        while count_passports > 0:
            if PassportSystem.series:
                number_passport = PassportSystem.create_random_number(6)
                if self.is_dublicate(number_passport):
                    continue
                passport = Passport(PassportSystem.series,number_passport,input('Введите имя владельца паспорта\n'))
                PassportSystem.list_numbers.append(passport)
                print("Создан паспорт",passport)
            count_passports -= 1

    def is_dublicate(self,number):
        for passport in PassportSystem.list_numbers:
            if passport.number == number and passport.series == PassportSystem.series:
                return True
        return False

    @staticmethod
    def create_random_number(count_numbers):
        """Полуаем строку с необходимым количеством цифр"""
        s = ""
        for _ in range(count_numbers):
            s += str(random.randint(0,9))
        return s


    def create_series(self):
        answer = input("Для ввода серии паспорта вручную введите H или A - для автоматического заполнения").lower()
        match answer:
            case "a":
                PassportSystem.series = PassportSystem.create_random_number(4)
            case "h":
                while 1:
                    answer = input('Введите серию паспорта в виде NN-NN')
                    if PassportSystem.is_valid(answer):
                        PassportSystem.series = answer
                        break
                    print("Вы ввели серию паспорта неверно!")
            case _:
                print("Вы выбрали некорректное значение!")

    @classmethod
    def find_owner(cls,s_n):
        mas = s_n.split()
        for passport in PassportSystem.list_numbers:
            if passport.series == mas[0] and passport.number == mas[1]:
                return passport.fio
        return "Паспорт в системе не найден!"




    @staticmethod
    def is_valid(s:str):
        """Проверка на серию паспорта"""
        mas = s.split("-")
        if len(mas) == 2:
            for item in mas:
                for i in item:
                    if not i.isdigit():
                        return False
            return True
        return False

        # return re.match(r'^\d{2}-\d{2}$', s)


# print(PassportSystem.is_valid("22-11"))