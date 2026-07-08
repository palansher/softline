import datetime
import json

import jwt
from flask import Flask,request,jsonify,render_template_string,Response



SECRET_KEY = 'SFDSKFSKFJSLFDFGDFGFJHGK'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <h2>Проверка токена</h2>
        <form action="/greet" method="post">
            Токен:  <input type="text" name="token"><br>
            <button type="submit">Проверить</button>
        </form>    
    ''')

@app.route('/greet',methods=['POST'])
def greet():
   token = request.form['token']
   if not token:
       return jsonify({'message':'Токен отсутствует'}),400
   try:
       decoded = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
       return f'<h2>Привет, {decoded['user']}!</h2>'
   except jwt.ExpiredSignatureError:
       return jsonify({'message':'Токен истек'}),401
   except jwt.InvalidTokenError:
       return jsonify({'message': 'Токен неверный'}), 401
if __name__ == '__main__':
    app.run(debug=True,port=5001)