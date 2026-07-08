from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

persons = [
    {"id": "1", "fio": "Иванов", "salary": 150_00},
    {"id": "2", "fio": "Петров", "salary": 250_00},
    {"id": "2", "fio": "Сидоров", "salary": 250_00},
]


@app.route("/list_pesons", methods=["GET"])
def list_pesons():
    return jsonify(persons)


@app.route("/get_peson/<int:person_id>", methods=["GET"])
def get_peson_by_id(person_id):
    for person in persons:
        if person["id"] == person_id:
            return person
    return "Сотрудник не найден"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
