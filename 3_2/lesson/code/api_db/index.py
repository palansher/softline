from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Настройка подключения к PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="postgres",
    database="flask_shop",
    port="5433"
)


# ============= CRUD операции для item =============

@app.route('/items', methods=['GET'])
def get_all_items():
    """Получить все товары"""
    try:
        with connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM item ORDER BY item_id")
            items = cursor.fetchall()
            return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    """Получить товар по ID"""
    try:
        with connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM item WHERE item_id = %s", (item_id,))
            item = cursor.fetchone()

            if item:
                return jsonify(item)
            return jsonify({"error": "Товар не найден!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/items', methods=['POST'])
def add_item():
    """Добавить новый товар"""
    try:
        item_data = request.get_json()

        if not item_data:
            return jsonify({"error": "Нет данных для добавления"}), 400

        required_fields = ['title', 'price']
        for field in required_fields:
            if field not in item_data:
                return jsonify({"error": f"Отсутствует обязательное поле: {field}"}), 400

        with connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                           INSERT INTO item (title, price, info, photo)
                           VALUES (%s, %s, %s, %s)
                           """, (
                               item_data.get('title'),
                               item_data.get('price'),
                               item_data.get('info'),
                               item_data.get('photo')
                           ))

            connection.commit()

            # Просто возвращаем успех
            return jsonify({"status": "success", "message": "Товар успешно добавлен"}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    """Обновить товар"""
    try:
        item_data = request.get_json()

        if not item_data:
            return jsonify({"error": "Нет данных для обновления"}), 400

        with connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)

            # Проверяем существование товара
            cursor.execute("SELECT * FROM item WHERE item_id = %s", (item_id,))
            existing_item = cursor.fetchone()

            if not existing_item:
                return jsonify({"error": "Товар не найден!"}), 404

            # Обновляем только переданные поля
            update_fields = []
            update_values = []

            if 'title' in item_data:
                update_fields.append("title = %s")
                update_values.append(item_data['title'])
            if 'price' in item_data:
                update_fields.append("price = %s")
                update_values.append(item_data['price'])
            if 'info' in item_data:
                update_fields.append("info = %s")
                update_values.append(item_data['info'])
            if 'photo' in item_data:
                update_fields.append("photo = %s")
                update_values.append(item_data['photo'])

            if not update_fields:
                return jsonify({"error": "Нет полей для обновления"}), 400

            update_values.append(item_id)
            query = f"UPDATE item SET {', '.join(update_fields)} WHERE item_id = %s"

            cursor.execute(query, update_values)
            connection.commit()

            # Получаем обновленный товар
            cursor.execute("SELECT * FROM item WHERE item_id = %s", (item_id,))
            updated_item = cursor.fetchone()

            return jsonify(updated_item), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Удалить товар"""
    try:
        with connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)

            # Проверяем существование товара
            cursor.execute("SELECT * FROM item WHERE item_id = %s", (item_id,))
            existing_item = cursor.fetchone()

            if not existing_item:
                return jsonify({"error": "Товар не найден!"}), 404

            cursor.execute("DELETE FROM item WHERE item_id = %s", (item_id,))
            connection.commit()

            return jsonify({
                "message": "Товар успешно удален",
                "deleted_item": existing_item  # Возвращаем сохраненный ранее товар
            }), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8087)