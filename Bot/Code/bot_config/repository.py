import sqlite3

def check_user(
    db_path: str,
    table_name: str,
    check_graph: str,
    param_to_check,
):
    with sqlite3.connect(db_path) as db:
        cursor = db.execute(f"SELECT * FROM {table_name} WHERE {check_graph} = ?", (param_to_check,))
        result = cursor.fetchall()

    return result



def insert_row(
    db_path: str,
    table_name: str, 
    **kwargs):
    import sqlite3
    columns = ', '.join(kwargs.keys())
    values = ', '.join(['?' for _ in kwargs.values()])

    sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(sql_query, tuple(kwargs.values()))

    conn.commit()
    conn.close()


def update_value(
    database_path: str, 
    table_name: str,
    search_column: str, 
    param_to_search,
    column_to_change: str,
    new_value
    ):
    import sqlite3
    
    # Подключение к базе данных
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Получаем текущее значение столбца, чтобы затем обновить только одну ячейку
    select_query = f"SELECT {column_to_change} FROM {table_name} WHERE {search_column} = ?"
    cursor.execute(select_query, (param_to_search,))
    current_value = cursor.fetchone()

    if current_value is not None:
        current_value = current_value[0]
        if current_value != new_value:
            update_query = f"UPDATE {table_name} SET {column_to_change} = ? WHERE {search_column} = ?"
            cursor.execute(update_query, (new_value, param_to_search))
            conn.commit()
            print("Значение успешно обновлено.")
        else:
            print("Новое значение совпадает с текущим значением.")
    else:
        print("Строка с указанным значением не найдена.")

    # Закрытие соединения
    conn.close()


def get_value_by_search(
    database_path: str, 
    table_name: str, 
    search_column: str, 
    search_value, 
    target_column
    ):
    import sqlite3
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    select_query = f"SELECT {target_column} FROM {table_name} WHERE {search_column} = ?"
    cursor.execute(select_query, (search_value,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    else:
        return None


def get_rows_by_value(
    database_path: str, 
    table_name: str, 
    search_column: str, 
    search_value, 
    sort_by: str = None,
    ):
    import sqlite3
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    sort = f'ORDER BY {sort_by}' if sort_by is not None else ''
    select_query = f"SELECT * FROM {table_name} WHERE {search_column} = ? {sort}"
    cursor.execute(select_query, (search_value,))
    rows = cursor.fetchall()
    return rows
