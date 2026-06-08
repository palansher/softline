from flask import Flask, request,render_template

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('form_ajax_v2.html')
    a = int(request.form.get('a',0))
    b = int(request.form.get('b',0))
    return str(a+b)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)