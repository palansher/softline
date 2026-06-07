from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Добрый день! Это ответ production сервера!</h1>'

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8081), app)
    http_server.serve_forever()