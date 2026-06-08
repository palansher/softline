from flask import Flask, render_template, request,redirect

app = Flask(__name__)

@app.route('/test_api',methods=['GET','POST'])
def test_api():
    if request.method == 'GET':
        return {
            'status': 'success',
            'body_answer':'Тестовый ответ на запрос',
            'method': request.method
        }
    return {
        'status': 'success POST',
        'body_answer': 'Тестовый ответ на post запрос',
        'body_request': request.json
    }

# Обработка запроса с параметром
@app.route('/test_api/<int:item_id>',methods=['GET','PUT'])
def demo_api(item_id):
    if request.method == 'GET':
        return {
            'status': 'success',
            'id':item_id,
            'body_answer':'Запрос успешно обработан!'
        }
    return {
        'status': 'success PUT',
        'id':item_id,
        'body_request': 'Информация от клиента для сервиса!'
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)