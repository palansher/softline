
# Как заставить Flask хранить сессии на сервере (в каталоге)?
# Если вам нужно хранить в сессии много данных (напомню, кука ограничена 4 Кб) или вы не хотите отдавать эти данные клиенту, дефолтное поведение нужно изменить.
# Для этого используется популярное расширение Flask-Session. С его помощью можно настроить хранение в файловую систему сервера.
# Как это сделать:
# Установите библиотеку: pip install Flask-Session

from flask import Flask, session
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'sdfjlsfj234234!@sg'

# Настраиваем хранение в файлы на сервере
app.config["SESSION_TYPE"] = "filesystem"

# Указываем конкретный каталог для сессий (опционально)
# app.config["SESSION_FILE_DIR"] = "./flask_sessions"

# Если вы укажете app.config["SESSION_FILE_DIR"] = "./flask_sessions", то в корне вашего проекта создастся папка flask_sessions, 
# внутри которой Flask начнет плодить файлы со случайными длинными именами. В этих файлах и будут лежать данные.

# Если этот параметр не указывать, но оставить SESSION_TYPE = "filesystem", Flask-Session создаст в корне проекта папку по умолчанию 
# с именем flask_session (в единственном числе) и будет складывать всё туда.


# Альтернативный вариант (через init_app)
# Если вы создаете приложение через фабрику функций (что часто используется в крупных проектах), Session объявляется глобально, а инициализируется позже:

# Python
# from flask import Flask
# from flask_session import Session

# # Создаем пустой объект сессии
# sess = Session()


# def create_app():
#     app = Flask(__name__)
#     app.config["SESSION_TYPE"] = "filesystem"

#     # Инициализируем приложение внутри фабрики
#     sess.init_app(app)

#     return app
# Итог:
# Вы используете Session ровно один раз в конфигурационной части кода (как Session(app) или sess.init_app(app)), чтобы активировать серверное хранение.
# Внутри самих роутов (@app.route) вы продолжаете использовать стандартный объект session из самого Flask.

Session(app)

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
# ситемный словарь config
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=40)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8084)