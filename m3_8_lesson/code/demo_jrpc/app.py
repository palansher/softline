import json

import flask
from flask import Response

from calc_service import CalcService

app = flask.Flask(__name__)

calc = CalcService()

@app.route('/rpc',methods=['POST'])
def rpc():
    body_request = flask.request.get_json(force=True)
    method = body_request["method"] #multiple
    parameters = body_request["params"] #параметры a и b
    result = get_result(method,parameters)
    response = {
        "jsonrpc": "2.0",
        "answer": result
    }
    return Response(json.dumps(response), mimetype="application/json")

def get_result(method:str,params) -> object:
    if method == "multiple":
        a = params.get("a")
        b = params.get("b")
        return calc.multiple(a, b)
    raise Exception("Invalid method")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)