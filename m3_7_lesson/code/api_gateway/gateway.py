from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

WAREHOUSE = "http://127.0.0.1:5002"
CATALOG = "http://127.0.0.1:5001"

data_catalog = None
data_warehouse = None

@app.route("/api/item/<int:id>", methods=["GET"])
def get_full_info(id):
    # Коннектимся к каталог и получаем товар из каталога
    try:
        data = requests.get(f"{CATALOG}/item/{id}",timeout=2)
        if data.status_code == 200:
            data_catalog = data.json()
        elif data.status_code == 404:
            return jsonify({"error":"item not found in catalog"})
    except requests.exceptions.RequestException as e:
        return jsonify({"Микросервис Каталог не доступен!"})

    # Коннектимся к складу и получаем информацию из него
    try:
        data_item_from_warehouse = requests.get(f"{WAREHOUSE}/warehouse/{id}", timeout=2)
        if data_item_from_warehouse.status_code == 200:
            data_warehouse = data_item_from_warehouse.json()
        elif data_item_from_warehouse.status_code == 404:
            data_warehouse = {"quantity":0,"status":"unavailable"}

    except requests.exceptions.RequestException as e:
        data_warehouse = {"quantity":0,"status":str(e)}

    common_response = {
        'id':id,
        'title':data_catalog['title'],
        'price':data_catalog['price'],
        'quantity':data_warehouse['quantity'],
        "status":data_warehouse['status']
    }
    return jsonify(common_response),200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)