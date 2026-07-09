from flask import Flask, request, jsonify  # render_template, redirect

app = Flask(__name__)

persons = [
    {"id": 1, "fio": "Иванов", "salary": 150_00},
    {"id": 2, "fio": "Петров", "salary": 250_00},
    {"id": 3, "fio": "Сидоров", "salary": 250_00},
]


@app.route("/list_pesons", methods=["GET"])
def list_pesons():
    return jsonify(persons)


@app.route("/get_person/<int:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    for person in persons:
        if person["id"] == person_id:
            return person
    return "Сотрудник не найден"


@app.route("/add_person", methods=["POST"])
def add_person():
    person = request.get_json()  # получили тело запроса
    if person:
        # print(person)
        # return {}
        persons.append(person)
        return persons
    return "Ошибка при добавлении"


@app.route("/update_person/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    person = request.get_json()  # получили тело запроса
    if person:
        for i, person in enumerate(persons):
            if person["id"] == person_id:
                persons[i] = person
                return persons
    return "Ошибка при обновлении"


@app.route("/delete_person/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    for i, person in enumerate(persons):
        if person["id"] == person_id:
            persons.pop(i)
            return persons
    return "Ошибка при удалении сотрудника"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
