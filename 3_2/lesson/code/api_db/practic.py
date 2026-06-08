import psycopg2
from flask import Flask, request

app = Flask(__name__)

conn = psycopg2.connect(
    host='localhost',
    database='mydatabase',
    user='myuser',
    password='mypassword',
    port=5432
)


@app.route('/task', methods=['GET'])
def get_tasks():
    query = """
        select * from test.daily_planner
    """
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    return cursor.fetchall()

@app.route('/get_task/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    query = f"""
            select * from test.daily_planner where id = %s
        """
    cursor = conn.cursor()
    cursor.execute(query, (task_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        columns = ['id', 'title', 'info', 'date_plan']
        task_dict = dict(zip(columns, result))
        return task_dict
    else:
        return []

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.get_json()
    if task:
        query = f"""
            INSERT INTO test.daily_planner (title, info, date_plan)
            VALUES (%s, %s, %s)
                """
        cursor = conn.cursor()
        cursor.execute(query, (task['title'], task['info'], task['date_plan']))
        conn.commit()

        return 'Задача добавлена'
    return 'Ошибка добавления'


@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    update_task = request.get_json()

    if update_task:
        query = f"""
            UPDATE test.daily_planner 
            SET title = %s, info = %s, date_plan = %s
            WHERE id = %s
        """
        cursor = conn.cursor()
        cursor.execute(query, (update_task['title'], update_task['info'], update_task['date_plan'], task_id))
        conn.commit()

        if cursor.rowcount == 0:
            return 'ID не найден'

        cursor.close()
        return 'Задача обновлена'
    return 'Ошибка обновления'

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    query = f"""
            delete from test.daily_planner where id = %s
        """
    cursor = conn.cursor()
    cursor.execute(query, (task_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return 'Задача не найдена'

    return 'Задача удалена'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)