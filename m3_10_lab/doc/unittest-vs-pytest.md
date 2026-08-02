# pytest vs unit_test 

`pytest` ищет файлы через файловую систему, а не через строгий `import`, поэтому он не падает от некорректных имён сторонних файлов. Главный плюс: **`pytest` нативно поддерживает и умеет запускать тесты, написанные на `unittest**` (`unittest.TestCase`).

Замените в настройках workspace (`softline.code-workspace` или `.vscode/settings.json`) параметры тестирования:

```json
"python.testing.unittestEnabled": false,
"python.testing.pytestEnabled": true,
"python.testing.pytestArgs": [
    "m3_10_lab"
]

```

*(Указание `"m3_10_lab"` в `pytestArgs` заставит `pytest` искать тесты конкретно в этой папке, игнорируя остальной проект).*

---

## ⚔️ Чем отличается `unittest` от `pytest`

| Критерий | `unittest` | `pytest` |
| --- | --- | --- |
| **Происхождение** | Встроен в стандартную библиотеку Python (`stdlib`). | Сторонняя библиотека (`pip install pytest`). |
| **Стиль написания** | **ООП-стиль.** Обязательно создавать класс, наследуемый от `unittest.TestCase`. | **Функциональный.** Достаточно написать обычную функцию `def test_*()`. |
| **Проверки (Assertions)** | Набор специальных методов: `self.assertEqual(a, b)`, `self.assertTrue(x)`. | Стандартный оператор `assert a == b`. `pytest` сам перехватывает его и выдаёт подробный diff при падении. |
| **Фикстуры (setUp/tearDown)** | Жесткие методы `setUp()`, `tearDown()`, `setUpClass()`. | Гибкие фикстуры через декоратор `@pytest.fixture` с поддержкой внедрения зависимостей. |
| **Параметризация** | Требует сторонних пакетов или подклассов. | Из коробки через `@pytest.mark.parametrize`. |
| **Совместимость** | Понимает только свои тесты. | **Универсален:** запускает и свои тесты, и тесты `unittest`. |

### Пример одного и того же теста:

* **На `unittest`:**
```python
import unittest


class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 2, 4)

```


* **На `pytest`:**
```python
def test_add():
    assert 2 + 2 == 4

```