import os
import re
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'admin')

# Параметры подключения к БД
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'webstore')
DB_USER = os.environ.get('DB_USER', 'webstore')
DB_PASS = os.environ.get('DB_PASS', 'webstore')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, phone, name, is_admin FROM customers WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart

def clear_cart():
    session.pop('cart', None)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user or user['is_admin'] != 1:
            flash('Доступ запрещён.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not get_current_user():
            flash('Пожалуйста, войдите.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

# ------------------ Регистрация ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password')
        name = request.form.get('name', '').strip()
        if not phone or not password or not name:
            flash('Заполните все поля', 'danger')
            return render_template('register.html')
        if not re.match(r'^\+?\d{10,15}$', phone):
            flash('Некорректный телефон', 'danger')
            return render_template('register.html')
        pwd_hash = generate_password_hash(password)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO customers (phone, password_hash, name, is_admin) VALUES (%s, %s, %s, 0)',
                (phone, pwd_hash, name)
            )
            conn.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('Телефон уже существует', 'danger')
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, phone, password_hash, is_admin FROM customers WHERE phone = %s', (phone,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Добро пожаловать!', 'success')
            next_page = request.args.get('next')
            # Если администратор – в админку, иначе – на главную (или next)
            if user['is_admin'] == 1:
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                return redirect(next_page or url_for('index'))
        else:
            flash('Неверный телефон или пароль', 'danger')
    return render_template('login.html')

# ------------------ (выход из кабинета) ------------------
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли', 'info')
    return redirect(url_for('index'))

# ------------------ ТОВАРЫ И КОРЗИНА ------------------
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=products)

# ------------------ (карточка продукта) ------------------
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)

# ------------------ (добавление в корзину) ------------------
@app.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM products WHERE id = %s', (product_id,))
    product = cur.fetchone()
    print(product)
    cur.close()
    conn.close()
    if not product:
        flash('Товар не найден', 'danger')
        return redirect(url_for('index'))
    cart = get_cart()
    key = str(product_id)           # ключ – строка
    cart[key] = cart.get(key, 0) + 1
    save_cart(cart)
    flash(f'Товар "{product["name"]}" добавлен', 'success')
    return redirect(request.referrer or url_for('index'))

# ------------------ (удаление из корзины) ------------------
@app.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    if key in cart:
        del cart[key]
        save_cart(cart)
        flash('Товар удалён', 'info')
    return redirect(url_for('view_cart'))

# ------------------ (обновление корзины) ------------------
@app.route('/cart/update', methods=['POST'])
def update_cart():
    cart = get_cart()
    for key, value in request.form.items():
        if key.startswith('qty_'):
            product_id = key.split('_')[1]   # строка
            qty = int(value)
            if qty <= 0:
                cart.pop(product_id, None)
            else:
                cart[product_id] = qty
    save_cart(cart)
    flash('Корзина обновлена', 'success')
    return redirect(url_for('view_cart'))

# ------------------ (корзина) ------------------
@app.route('/cart')
def view_cart():
    cart = get_cart()
    cart_items = []
    total = 0.0
    if cart:
        conn = get_db_connection()
        cur = conn.cursor()
        for product_id_str, qty in cart.items():
            product_id = int(product_id_str)   # преобразуем в int для SQL
            cur.execute('SELECT id, name, price, image_url FROM products WHERE id = %s', (product_id,))
            product = cur.fetchone()
            if product:
                subtotal = float(product['price']) * qty
                total += subtotal
                cart_items.append({
                    'product': product,
                    'quantity': qty,
                    'subtotal': subtotal
                })
        cur.close()
        conn.close()
    return render_template('cart.html', cart_items=cart_items, total=total)

# ------------------ ЗАКАЗЫ ------------------
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash('Корзина пуста', 'warning')
        return redirect(url_for('index'))

    user = get_current_user()
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO orders (customer_id, status) VALUES (%s, %s) RETURNING id', (user['id'], 'новый'))
        order_id = cur.fetchone()['id']

        total_amount = 0.0
        ok = True
        for product_id, quantity in cart.items():
            cur.execute('SELECT name, price, stock FROM products WHERE id = %s', (product_id,))
            product = cur.fetchone()
            if not product or product['stock'] < quantity:
                flash(f'Недостаточно: {product["name"] if product else "товар"}', 'danger')
                ok = False
                break
            price = float(product['price'])
            total_amount += price * quantity
            cur.execute('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)',
                        (order_id, product_id, quantity, price))
            cur.execute('UPDATE products SET stock = stock - %s WHERE id = %s', (quantity, product_id))
        if ok:
            cur.execute('UPDATE orders SET total_amount = %s WHERE id = %s', (total_amount, order_id))
            conn.commit()
            clear_cart()
            flash('Заказ оформлен!', 'success')
            cur.close()
            conn.close()
            return redirect(url_for('orders'))
        else:
            conn.rollback()
            cur.close()
            conn.close()
            return redirect(url_for('view_cart'))

    cart_items = []
    total = 0.0
    conn = get_db_connection()
    cur = conn.cursor()
    for product_id, qty in cart.items():
        cur.execute('SELECT id, name, price, image_url FROM products WHERE id = %s', (product_id,))
        product = cur.fetchone()
        if product:
            subtotal = float(product['price']) * qty
            total += subtotal
            cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
    cur.close()
    conn.close()
    return render_template('checkout.html', cart_items=cart_items, total=total, user=user)

# ------------------ (Мои заказы) ------------------
@app.route('/orders')
@login_required
def orders():
    user = get_current_user()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC', (user['id'],))
    orders = cur.fetchall()
    for order in orders:
        cur.execute('''
            SELECT oi.quantity, oi.price, p.name, p.id
            FROM order_items oi JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        ''', (order['id'],))
        order['items'] = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('orders.html', orders=orders)

# ------------------ АДМИНКА ------------------
@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as cnt FROM products')
    total_products = cur.fetchone()['cnt']
    cur.execute('SELECT COUNT(*) as cnt FROM customers')
    total_customers = cur.fetchone()['cnt']
    cur.execute('SELECT COUNT(*) as cnt FROM orders')
    total_orders = cur.fetchone()['cnt']
    cur.execute('SELECT COALESCE(SUM(total_amount), 0) as sum FROM orders')
    total_revenue = float(cur.fetchone()['sum'])
    cur.close()
    conn.close()
    return render_template('admin_dashboard.html',
                           total_products=total_products,
                           total_customers=total_customers,
                           total_orders=total_orders,
                           total_revenue=total_revenue)

# ------------------ АДМИНКА (продукты) ------------------
@app.route('/admin/products')
@admin_required
def admin_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products ORDER BY id')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_products.html', products=products)

# ------------------ АДМИНКА (добавление продукта) ------------------
@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_product_add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image_url = request.form.get('image_url', 'images/default.jpg')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO products (name, description, price, stock, image_url) VALUES (%s, %s, %s, %s, %s)',
            (name, description, price, stock, image_url)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Товар добавлен', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_product_form.html', product=None)

# ------------------ АДМИНКА (редактирование продукта) ------------------
@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_product_edit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image_url = request.form.get('image_url', 'images/default.jpg')
        cur.execute(
            'UPDATE products SET name=%s, description=%s, price=%s, stock=%s, image_url=%s WHERE id=%s',
            (name, description, price, stock, image_url, id)
        )
        conn.commit()
        flash('Товар обновлён', 'success')
        cur.close()
        conn.close()
        return redirect(url_for('admin_products'))
    cur.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        abort(404)
    return render_template('admin_product_form.html', product=product)

# ------------------ АДМИНКА (удаление продукта) ------------------
@app.route('/admin/products/delete/<int:id>')
@admin_required
def admin_product_delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Товар удалён', 'success')
    return redirect(url_for('admin_products'))

# ------------------ АДМИНКА (покупатели) ------------------
@app.route('/admin/customers')
@admin_required
def admin_customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, phone, name, created_at, is_admin FROM customers ORDER BY id')
    customers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_customers.html', customers=customers)

# ------------------ АДМИНКА (просмотр заказов) ------------------
@app.route('/admin/orders')
@admin_required
def admin_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.*, c.name AS customer_name, c.phone
        FROM orders o JOIN customers c ON o.customer_id = c.id
        ORDER BY o.order_date DESC
    ''')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_orders.html', orders=orders)

# ------------------ АДМИНКА (просмотр заказа) ------------------
@app.route('/admin/order/<int:id>')
@admin_required
def admin_order_detail(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.*, c.name AS customer_name, c.phone
        FROM orders o JOIN customers c ON o.customer_id = c.id
        WHERE o.id = %s
    ''', (id,))
    order = cur.fetchone()
    if not order:
        abort(404)
    cur.execute('''
        SELECT oi.quantity, oi.price, p.name, p.id
        FROM order_items oi JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    ''', (id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_order_detail.html', order=order, items=items)

# ------------------ ОБРАТНАЯ СВЯЗЬ ------------------
@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form.get('name', '').strip()
    vin = request.form.get('vin', '').strip()
    message = request.form.get('message', '').strip()
    if not name or not message:
        flash('Заполните имя и сообщение', 'danger')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO feedbacks (name, vin, message) VALUES (%s, %s, %s)',
        (name, vin, message)
    )
    conn.commit()
    cur.close()
    conn.close()
    flash('Ваше сообщение отправлено! Мы свяжемся с вами.', 'success')
    return redirect(url_for('index'))

# ------------------ АДМИНКА (просмотр заявок) ------------------
@app.route('/admin/feedbacks')
@admin_required
def admin_feedbacks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM feedbacks ORDER BY created_at DESC')
    feedbacks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_feedbacks.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)