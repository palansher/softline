# визуализация графиков Visual Studio Code

## Проблема


```
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

animals = pd.read_csv(script_dir / "animals.csv")
animals['water_need'].plot.box()
plt.title('Тестовый график')
plt.show()
```

это я запускаю Visual Studio Code на Windows, но код работает на удаленной remote  SSH Ubuntu.

Код выполняется нормально без ошибок, но графика я не вижу. Возможно, потому что Ubuntu это LTS.

Можно ли отобразить этот график в среде Visual Studio Code? Возможно, есть какой-то плагин?

## Решение

Проблема не в том, что на сервере установлена Ubuntu LTS, а в том, как устроена работа по SSH.

Удаленный сервер по умолчанию не имеет графического окружения (X11/Wayland), поэтому `plt.show()` либо тихо пытается сгенерировать окно «в никуда», либо задействует «слепой» бекенд (Agg), который просто сохраняет график в память, но не выводит его на экран.

Отобразить график прямо внутри VS Code можно — и для этого **не нужно настраивать сложные X11-серверы вроде VcXsrv или PuTTY**. В VS Code уже встроен интерактивный просмотрщик графиков (*Interactive Window / Plot Viewer*).

Вот **3 проверенных способа**, от самого удобного к альтернативным:

---

### Способ 1. Использование VS Code Interactive Window (Рекомендуемый)

VS Code умеет выполнять код блоками и перехватывать вывод Matplotlib прямо в интерфейсе.

1. Установите на **удаленном сервере** пакет `ipykernel`:

```bash
pip install ipykernel

```

1. В файле с кодом добавьте спец-комментарий `# %%` перед вашим кодом, чтобы превратить его в «ячейку» (как в Jupyter):

```python
# %%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

script_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

animals = pd.read_csv(script_dir / "animals.csv")
animals["water_need"].plot.box()
plt.title("Тестовый график")
plt.show()

```

1. Над строчкой `# %%` появится надпись **Run Cell**. Нажмите её (или нажмите `Shift + Enter`).
2. VS Code предложит выбрать Python Kernel, откроет справа панель **Interactive** и нарисует график прямо там с возможностью зума, копирования и сохранения.

---

### Способ 2. Запуск файла как Jupyter Notebook (`.ipynb`)

Если вы переименуете файл из `.py` в `.ipynb` (или создадите Jupyter Notebook):

* Все графики через `plt.show()` или даже просто вывод `animals['water_need'].plot.box()` будут автоматически рендериться прямо в редакторе VS Code без дополнительных настроек.

---

### Способ 3. Автоматическое сохранение во временный файл (Если нужен строго чистый `.py` скрипт)

Если вам обязательно нужно запускать обычный Python-скрипт через терминал (`python main.py`), то вместо `plt.show()` график сохраняется в файл, а просмотрщик VS Code откроет его автоматически:

```python
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

script_dir = Path(__file__).resolve().parent

animals = pd.read_csv(script_dir / "animals.csv")
animals["water_need"].plot.box()
plt.title("Тестовый график")

# Сохраняем рядом и не блокируем выполнение
output_plot = script_dir / "plot.png"
plt.savefig(output_plot)
print(f"График сохранен в {output_plot}")

```

В VS Code слева в проводнике файлов появится `plot.png`. Кликнув по нему, вы увидите изображение.

---

> **Итог:** Самый комфортный путь при разработке в VS Code — использовать **Interactive Window (`# %%`)** или `.ipynb` ноутбуки. В этом случае расширение *Python / Jupyter* для VS Code всё сделает за вас без проброса GUI с удаленной Ubuntu.
