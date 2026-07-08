# {
#     "login":"test",
#     "password":"password"
# }
import datetime

import jwt
from flask import Flask,request,jsonify

SECRET_KEY = 'SFDSKFSKFJSLFDFGDFGFJHGK'

app = Flask(__name__)

@app.route('/login',methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('login') or not auth.get('password'):
        return jsonify({'message':'Ошибка получения данных аутентификации'})

    token = jwt.encode(
        payload={'user': auth['login'],'exp': datetime.datetime.now() + datetime.timedelta(minutes=15)},
    key=SECRET_KEY,algorithm='HS256'
    )
    return jsonify({'token':token})

if __name__ == '__main__':
    app.run(debug=True,port=8080)