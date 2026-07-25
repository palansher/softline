import os
import subprocess
from pathlib import Path

import pandas as pd

# Получаем путь к папке, где лежит текущий скрипт
script_dir = Path(__file__).parent

def clear_screen():
    # Определяем команду в зависимости от ОС
    command = "cls" if os.name == "nt" else "clear"

    # Вызываем команду безопасно без использования shell=True
    subprocess.run([command], check=False)


store = pd.DataFrame(
    {
        "mark": ["Audi", "VW", "BMW"],
        "model": ["A6", "Golf", "X5"],
        "prices": [1000, 900, 1200],
    }
)



clear_screen()

# conda install openpyxl
# store.to_excel("cars.xlsx",index=False,sheet_name="Автомобили")

# Можем выбрать имена колонок для вывода.
cars = pd.read_excel(script_dir / "cars.xlsx", usecols="A,C")
print(cars)
