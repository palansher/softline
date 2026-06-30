import datetime

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html',cur_date=datetime.date.today())

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)