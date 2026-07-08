import psycopg2
import psycopg2.extras
from config import Config


def get_db():
    """Возвращает новое соединение с БД."""
    return psycopg2.connect(**Config.db_config())


def query(sql, params=None, fetchone=False, fetchall=False, commit=False):
    """
    Универсальная функция выполнения SQL-запросов.

    :param sql:      SQL-строка
    :param params:   параметры запроса
    :param fetchone: вернуть одну строку
    :param fetchall: вернуть все строки
    :param commit:   зафиксировать транзакцию
    :return:         результат запроса или None
    """
    conn = get_db()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(sql, params)

        if commit:
            conn.commit()
            try:
                result = (cur.fetchone() if fetchone
                          else cur.fetchall() if fetchall
                          else None)
            except Exception:
                result = None
            return result

        if fetchone:
            return cur.fetchone()
        if fetchall:
            return cur.fetchall()
        return None

    except Exception as exc:
        conn.rollback()
        raise exc
    finally:
        cur.close()
        conn.close()
