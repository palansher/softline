# Курсор в многопоточных приложениях

Вот мы и наступили на вторую классическую ловушку при работе с базами данных во многопоточных приложениях.

Ошибка `psycopg2.InterfaceError: cursor already closed` (курсор уже закрыт) возникла как раз из-за того, что мы **убрали блок `with connection:` из файла инициализации**, но логика его работы была завязана на одну важную деталь.

---

## Почему это произошло

Раньше файл `connect_db.py` выглядел так:

```python
with connection:
    cursor = connection.cursor(cursor_factory=RealDictCursor)

```

Когда мы убрали `with connection:`, мы сделали всё правильно с точки зрения транзакций, но упустили то, как Python работает с контекстными менеджерами на уровне глобальных переменных.

В старом коде блок `with` открывался, создавал курсор, но **он никогда не закрывался**, потому что скрипт инициализации выполнялся один раз при старте, и этот единственный курсор становился «вечным» глобальным объектом для всего приложения Flask.

**Но почему он теперь пишет, что закрыт?**
Поскольку Flask работает в многопоточном режиме (`debug=True`), каждый раз, когда вы перезагружаете страницу или открываете карточку товара, Flask может обрабатывать этот запрос в новом потоке. Одиночный глобальный `cursor`, созданный без контекста, при первом же сбое или конкурентном запросе от браузера (например, когда браузер одновременно запрашивает саму страницу и её favicon.ico) просто уничтожается или закрывается базой данных ради безопасности. И при следующем клике Flask пытается вызвать уже мертвый объект.

---

## Как это исправить архитектурно правильно?

В веб-приложениях (Flask, FastAPI, Django) **никогда нельзя использовать один глобальный курсор на всё приложение**.

* **Соединение (`connection`)** — должно быть глобальным (оно держит общую трубу до базы).
* **Курсор (`cursor`)** — должен создаваться **индивидуально внутри каждого HTTP-запроса** и закрываться сразу после того, как запрос отработал.

Давайте приведем архитектуру к промышленному стандарту.

### Шаг 1. Чистим глобальный `connect_db.py`

В этом файле должно создаваться только подключение. Курсор отсюда мы убираем.

```python
import psycopg2

connection = psycopg2.connect(
    host="vm-perepechenko01.brg.loc",
    user="postgres",
    password="admin",
    database="shop_db_hw3_1",
    port="5432",
)

# Оставляем автокоммит — он защищает от зависших локов
connection.autocommit = True

```

### Шаг 2. Переносим создание курсора в роуты `app.py`

Теперь внутри каждого роута мы будем запрашивать у глобального `connection` свежий курсор через конструкцию `with connection.cursor(...) as cursor:`.

Этот контекстный менеджер гарантирует: как только роут отработал (или упал с ошибкой) — курсор **автоматически закроется**, не мешая другим потокам веб-сервера.

Обновите ваши функции в `app.py`:

```python
from flask import Flask, render_template
from psycopg2.extras import RealDictCursor
from connect_db import connection  # Импортируем соединение вместо курсора

app = Flask(__name__)

@app.route("/")
def index() -> str:
    return render_template("main.html")

@app.route("/contacts")
def contacts() -> str:
    return render_template("contacts.html")

@app.route("/catalog")
def catalog():
    sql = "SELECT * FROM v_catalog_display ORDER BY price DESC;"
    
    # Создаем локальный курсор для конкретного запроса
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        
    # Здесь курсор уже автоматически и безопасно закрылся
    return render_template("catalog.html", items=data)

@app.route("/catalog/<int:car_id>")
def car_detail(car_id: int):
    sql = "SELECT * FROM v_catalog_display WHERE car_id = %s;"
    
    # Создаем локальный курсор для конкретного просмотра машины
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql, (car_id,))
        car = cursor.fetchone()

    if not car:
        return "Автомобиль не найден", 404

    return render_template("car-detail.html", car=car)

@app.template_filter("format_price")
def format_price(value):
    if value is None:
        return "0 ₽"
    return f"{int(value):,}".replace(",", " ") + " ₽"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8082)

```

## Что изменилось?

Обратите внимание на `with connection.cursor(...) as cursor:`. В отличие от `with connection` (который управляет транзакциями), контекстный менеджер **`with connection.cursor()`** управляет именно жизненным циклом самого курсора — он открывает его для выполнения запроса и гарантированно делает ему `.close()` на выходе из блока `with`.

Теперь код стал полностью потокобезопасным, и ошибка `cursor already closed` больше никогда не появится!
