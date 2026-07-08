from flask import Flask, render_template
from my_pool import *
app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM products')
        products = cur.fetchall()
        cur.close()
        return render_template('index.html', products=products)
    finally:
        return_db_connection(conn)  # Обязательно вернуть в пул!