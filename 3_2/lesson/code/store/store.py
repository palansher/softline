from flask import Flask, render_template, request,redirect

from connect_db import *

app = Flask(__name__)

@app.route('/')
def catalog():
    sql = 'select * from item'
    cursor.execute(sql)
    data = cursor.fetchall()
    if 'success' in request.args and request.args['success']:
        return render_template('index.html', success=True,items=data)
    return render_template('index.html', items=data)

@app.route('/add_cart')
def add_cart():
    id = request.args.get('id')
    if id.isdigit():
        id = int(id)
        sql = f'select id from cart where id={id}'
        cursor.execute(sql)
        item = cursor.fetchone()
        if item:
            query = f'UPDATE cart set quantity=quantity+1 where id={id}'
        else:
            query = f'insert into cart(item_id,quantity) values ({id},1)'
        cursor.execute(query)
        connection.commit()
        return redirect('/?success=True', code=302)
    return 'Ошибка!'

@app.route('/cart')
def cart():
    sql = 'SELECT title,price,quantity FROM item i INNER JOIN cart c ON i.item_id=c.item_id'
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('cart.html', items=data)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8087)