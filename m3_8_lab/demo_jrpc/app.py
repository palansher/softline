import json

import flask
from calc_service import CalcService
from flask import Response

app = flask.Flask(__name__)

calc = CalcService()

# Только POST запросы.
@app.route('/rpc',methods=['POST'])
def rpc():
    
    # Получаем тело запроса
    body_request = flask.request.get_json(force=True)
    method = body_request["method"] # наш метод multiple
    parameters = body_request["params"] #параметры a и b
    # Зная название метода и параметры, можно получить данные
    result = get_result(method,parameters)
    response = {
        "jsonrpc": "2.0",
        "answer": result
    }
    
    # return flask.jsonify(response)
    return Response(json.dumps(response), mimetype="application/json")
"""
Функция для получения результата
На вход принимаем название метода и параметры
"""
def get_result(method:str,params) -> object:
    if method == "multiple":
        a = params.get("a")
        b = params.get("b")
        return calc.multiple(a, b)
    raise Exception("Invalid method")  # noqa: TRY002

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)