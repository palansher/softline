# Добавим маршру, если товара конкретного нет
import connection
from flask import jsonify


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
