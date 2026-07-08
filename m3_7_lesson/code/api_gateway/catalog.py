from flask import Flask, request, jsonify

app = Flask(__name__)

ITEMS = {
    1:{"title":"Audi","price":1400},
    2:{"title":"BMW","price":1500},
    3:{"title":"VW","price":1200}
}

@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    item = ITEMS.get(id)
    if not item:
        return jsonify({'error':'item not found'}),404
    return jsonify(item)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)