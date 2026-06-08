
from flask import Flask, session
app = Flask(__name__)
app.secret_key = 'sdfjlsfj234234!@sg'
@app.route('/',methods=['GET','POST'])

def index():
   if 'count_visits' in session:
       session['count_visits'] += 1
   else:
       session['count_visits'] = 1
   return f'Вы посетили данную страницу {session["count_visits"]} раз'

# Для удаления элементов из сессии используем:
# 1) session.clear() #удаляем все элементы из сессии
# 2) session.pop('count_visits')

# Для установки времени жизни сессионной переменной на 40 минут:
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=40)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8084)