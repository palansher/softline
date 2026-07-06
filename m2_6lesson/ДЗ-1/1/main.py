from myCarNumberSystem import CarNumberSystem

gibdd = CarNumberSystem(5)
print(
    CarNumberSystem.find_owner(
        input("Введите номер автомобиля для поиска владельца:\n")
    )
)
