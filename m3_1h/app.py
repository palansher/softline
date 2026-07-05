import datetime

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return render_template('main.html')

# @app.route('/contacts')
# def contacts() -> str:
#     return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)