import datetime
import json

import jwt
from flask import Flask,request,jsonify,render_template_string,Response

USER = {
    'login':'admin',
    'password':'12345'
}

SECRET_KEY = 'SFDSKFSKFJSLFDFGDFGFJHGK'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <form action="/login" method="post">
            Логин: <input type="text" name="login"><br>
            Пароль: <input type="password" name="password"><br>
            <button type="submit">Войти</button>
        </form>    
    ''')

@app.route('/login',methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    data = False
    if not login or not password:
        data = {'message':'Необходимы логин и пароль'}
    elif login != USER['login'] and password != USER['password']:
        data = {'message': 'Логин и пароль неверны!'}
    if data:
        return Response(
            json.dumps(data,ensure_ascii=False),
            status=401,
            mimetype='application/json'
        )
    token = jwt.encode(
        payload={'user': login, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=15)},
        key=SECRET_KEY, algorithm='HS256'
    )
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(debug=True,port=5000)