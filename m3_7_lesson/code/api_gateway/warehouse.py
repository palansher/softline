"""Реализация склада"""
from flask import Flask, request, jsonify

app = Flask(__name__)

left_items = {
    1:{"quantity":5,"status":"active"},
    2:{"quantity":0,"status":"inactive"},
    3:{"quantity":10,"status":"active"}
}


@app.route('/warehouse/<int:id>', methods=['GET'])
def get_info_from_warehouse(id):
    item = left_items.get(id)
    if not item:
        return jsonify({'error':'no item'}),404
    return jsonify(item)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5002)