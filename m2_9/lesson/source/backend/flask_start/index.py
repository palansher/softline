import datetime

from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Добрый день! Это ответ сервера!</h1>'

# http://127.0.0.1:8080/test/Иван/25
@app.route('/test/<string:fio>/<int:age>')
def test(fio, age):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1>Привет, {fio}! Ваш год рождения: {datetime.datetime.now().year - age}</h1>
        </body>
        </html>
"""

"""
http://127.0.0.1:8080/get_params?fio=Иванов&age=25
"""
@app.route('/get_params')
def get_params():
    if request.method == 'GET': #проверяем, что был метод GET
        if 'fio' in request.args and 'age' in request.args: #проверяем, что передали необходимые параметры
          try:
              age = int(request.args['age'])
              if age > 0:
                  return f'{request.args["fio"]} родился в {datetime.datetime.now().year - age} году'
              return 'Возраст должен быть больше 0'
          except ValueError:
              return 'Возраст должен быть целым числом'
            
        # else:
    return 'Вы не передали GET параметры fio и age!!!'

"""
http://127.0.0.1:8080/sum?a=2&b=25
"""
@app.route('/sum')
def sum():
    if request.method == 'GET': #проверяем, что был метод GET
        if 'a' in request.args and 'b' in request.args: #проверяем, что передали необходимые параметры
          try:
            # со значением по умолчанию
            #   a = int(request.args.get('a',0)) 
              a = int(request.args['a'])
              b = int(request.args['b'])
              s = a + b
              return f'{a} + {b} = {s}'
          except ValueError:
              pass
        
    return 'Вы не передали GET параметры'

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8080)


# Передать 2 GET параметра с числами и найти сумму чисел. ВЫВЕСТИ информацию в виде:
# 2 + 3 = 5
