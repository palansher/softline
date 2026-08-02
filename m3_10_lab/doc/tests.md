# Юнит-тесты. Подготовка и проблемы

## Именование файлов с тестами

Главная причина, почему тест не отображается в списке — **дефисы (`-`) в имени файла `test_integration-3-10.py**`.

В панели **OUTPUT** на первом скриншоте видна ошибка:
`Failed to import test module... ModuleNotFoundError`

Для поиска и запуска тестов фреймворк `unittest` импортирует файлы как Python-модули. В Python дефис `-` является оператором вычитания, поэтому имена файлов с дефисами **не являются валидными именами модулей**, и `unittest` падает с ошибкой импорта, не успевая построить дерево тестов.

* **Было:** `test_integration-3-10.py`
* **Стало:** `test_integration_3_10.py`

---

## Отключите конфликт с Pytest в настройках

На вашем втором скриншоте (в `settings.json`) одновременно включены и `unittest`, и `pytest`:

```json
"python.testing.unittestEnabled": true,
"python.testing.pytestEnabled": true

```

Когда включены оба фреймворка, тестовый адаптер VS Code начинает путаться.

1. Откройте Настройки (`Ctrl + ,`).
2. Введите в поиск `python testing pytest enabled`.
3. Снимите галочку с **Python > Testing: Pytest Enabled** (оставьте только **Unittest Enabled**).

---

## Где находится конфигурация тестов в VS Code

Во вкладке **Testing** (колба слева) настройки не живут — там отображается только сформированное дерево тестов.

Конфигурация тестов в VS Code запускается и меняется двумя способами:

1. **Через Палитру команд:**

* Нажмите `Ctrl + Shift + P` (или `Cmd + Shift + P` на Mac).
* Наберите **Python: Configure Tests**.
* Выберите **unittest** $\rightarrow$ корневую папку `.` $\rightarrow$ шаблон `test_*.py`.

1. **В файле `settings.json` (который у вас уже настроен):**
У вас в файле `.vscode/settings.json` уже прописаны правильные аргументы для запуска:

```json
"python.testing.unittestEnabled": true,
"python.testing.unittestArgs": [
    "-v",
    "-s",
    ".",
    "-p",
    "test_*.py"
]

```
