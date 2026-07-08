from flask import Flask,request,jsonify

import requests

app = Flask(__name__)

@app.route('/process',methods=['POST'])
def process():
    data = request.json
    if not data or 'input_data' not in data:
        return jsonify({'error':'Неверные данные'}),400
    updated_data = data['input_data'].upper()
    return jsonify({'result':f'Обработанные данные: {updated_data}','original_data':data['input_data']})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4001)