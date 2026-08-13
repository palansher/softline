# Зачем нужны Pydantic-модели

- [Зачем нужны Pydantic-модели](#зачем-нужны-pydantic-модели)
  - [🎯 4 главные задачи `payload.py`](#-4-главные-задачи-payloadpy)
    - [Автоматическая валидация входящих данных (`CalculateRequest`)](#автоматическая-валидация-входящих-данных-calculaterequest)
    - [Формирование схемы ответов (`CalculateSuccessResponse` / `CalculateErrorResponse`)](#формирование-схемы-ответов-calculatesuccessresponse--calculateerrorresponse)
    - [Автоматическая генерация документации Swagger (`/docs`)](#автоматическая-генерация-документации-swagger-docs)
    - [Автодополнение и поддержка типов в IDE](#автодополнение-и-поддержка-типов-в-ide)

Файл **`payload.py`** содержит Pydantic-модели (схемы), которые выполняют роль **контракта данных** (DTO — *Data Transfer Object*) между клиентом (фронтендом) и бэкендом.

Простыми словами: эти классы строго описывают, **что именно сервер ожидает получить в JSON-запросе** и **что именно он гарантирует вернуть в ответе**.

---

## 🎯 4 главные задачи `payload.py`

### Автоматическая валидация входящих данных (`CalculateRequest`)

Когда клиент отправляет POST-запрос на `/api/calculate`, FastAPI сверяет тело запроса с классом `CalculateRequest`:

```python
class CalculateRequest(BaseModel):
    expression: str = Field(...)

```

* **Во Flask** приходилось проверять всё вручную:

```python
data = request.get_json()
if not data or "expression" not in data or not isinstance(data["expression"], str):
    return jsonify({"error": "Bad request"}), 400

```

* **В FastAPI** Pydantic сделает это автоматически. Если клиент передаст невалидный JSON (например, забыл поле `expression` или передал массив вместо строки), FastAPI моментально вернет клиенту понятный ответ со статусом `422 Unprocessable Entity`, даже не доходя до бизнес-логики.

---

### Формирование схемы ответов (`CalculateSuccessResponse` / `CalculateErrorResponse`)

Эти классы описывают структуру JSON-ответов при успехе и ошибках:

```python
class CalculateSuccessResponse(BaseModel):
    status: Literal["success"] = "success"
    result: int | float

```

Это гарантирует, что сервер всегда вернет стандартизированный ответ:

* В поле `status` всегда будет ровно строка `"success"`.
* В поле `result` будет только число (`int` или `float`), но не список или объект.

---

### Автоматическая генерация документации Swagger (`/docs`)

FastAPI использует эти классы для построения interactive-документации:

* Из аргументов `Field(description=..., examples=...)` берутся текстовые описания и примеры для интерфейса.
* В Swagger отображаются вкладки **Schemas**, где сторонний разработчик сразу видит формат данных без необходимости читать исходный код приложения.

---

### Автодополнение и поддержка типов в IDE

Благодаря наследованию от `BaseModel`, редактор кода (PyCharm / VS Code) "понимает" структуру объектов.

Когда вы пишете в `main.py`:

```python
async def calculate(payload: CalculateRequest):
    expr = payload.expression  # IDE сразу подскажет поле .expression и его тип str!

```

Это сводит к нулю риски опечататься в названиях полей JSON (например, написать `expresion` вместо `expression`).
