# 3.2

## содержание видео от 21.05.2026

### продлжение магазина на flask

### корзина покупок

### задание на доробатку магазина (админка, корзина, авторизация, система заказов и пр)

0:36

### веб сервисы (rest)на flask: 0:58:33
  
#### простой пример test_service.py

#### сложный пример index.py

```
  @app.route("/list_pesons", methods=["GET"])
  @app.route("/get_person/<int:person_id>", methods=["GET"])
  @app.route("/add_person", methods=["POST"])
  @app.route("/update_person/<int:person_id>", methods=["PUT"])
  @app.route("/delete_person/<int:person_id>", methods=["DELETE"])
```

используем with connection для автоматического закрытия соединений и курсоров (без .close)

### практика api db practic.py (tasks)

- 1:51:00 начиная  с Postgre 18 есть оператор RETURNING
db-postgress-returning.md
