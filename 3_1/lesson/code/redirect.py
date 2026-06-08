# import datetime

from flask import Flask, request,render_template,redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('form_poiskovik.html')
    poisk_value = request.form.get('poisk', "No value")
    if poisk_value == 'Yandex':
        data = request.form.get('query')
        if data:
            url = 'https://www.yandex.ru/search?text={}'.format(data)
            return redirect(url)
    return redirect(poisk_value)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8083)
   
