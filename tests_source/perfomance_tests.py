import pytest
import mysql.connector
import time

@pytest.fixture(scope='module')
def db_connection():
    cnx = mysql.connector.connect(
        user='mysql_user', 
        password='Qq123456!', 
        host='localhost', 
        database='test'
    )
    yield cnx
    cnx.close()

# Тесты, где сначала идёт запрос с индексом, а потом без индекса
def test_performance_select_like_index_first_1(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string77777'"

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Выполнение запроса с индексом
    start_time_with_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_with_index = time.time() - start_time_with_index

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    # Выполнение запроса без индекса
    start_time_no_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_no_index = time.time() - start_time_no_index

    cursor.close()

    # Вывод времени с выполнением запросов
    print(f"\nВремя выполнения запроса с индексом: {duration_with_index:.6f} секунд")
    print(f"Время выполнения запроса без индекса: {duration_no_index:.6f} секунд")

    # Проверка, что запрос с индексом выполняется быстрее
    assert duration_with_index < duration_no_index, "Запрос с индексом выполняется дольше, чем без индекса"

def test_performance_select_like_index_first_2(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string9____'"

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Выполнение запроса с индексом
    start_time_with_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_with_index = time.time() - start_time_with_index

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    # Выполнение запроса без индекса
    start_time_no_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_no_index = time.time() - start_time_no_index

    cursor.close()

    # Вывод времени с выполнением запросов
    print(f"\nВремя выполнения запроса с индексом: {duration_with_index:.6f} секунд")
    print(f"Время выполнения запроса без индекса: {duration_no_index:.6f} секунд")

    # Проверка, что запрос с индексом выполняется быстрее
    assert duration_with_index < duration_no_index, "Запрос с индексом выполняется дольше, чем без индекса"

def test_performance_select_like_index_first_3(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string7___7'"

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Выполнение запроса с индексом
    start_time_with_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_with_index = time.time() - start_time_with_index

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    # Выполнение запроса без индекса
    start_time_no_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_no_index = time.time() - start_time_no_index

    cursor.close()

    # Вывод времени с выполнением запросов
    print(f"\nВремя выполнения запроса с индексом: {duration_with_index:.6f} секунд")
    print(f"Время выполнения запроса без индекса: {duration_no_index:.6f} секунд")

    # Проверка, что запрос с индексом выполняется быстрее
    assert duration_with_index < duration_no_index, "Запрос с индексом выполняется дольше, чем без индекса"

# Тесты, где с начала идёт запрос без индекса, а потом с индексом (поменял порядок запросов)
def test_performance_select_like_index_last_1(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string77777'"

    # Выполнение запроса без индекса
    start_time_no_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_no_index = time.time() - start_time_no_index

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Выполнение запроса с индексом
    start_time_with_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_with_index = time.time() - start_time_with_index

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    cursor.close()

    # Вывод времени с выполнением запросов
    print(f"\nВремя выполнения запроса с индексом: {duration_with_index:.6f} секунд")
    print(f"Время выполнения запроса без индекса: {duration_no_index:.6f} секунд")

    # Проверка, что запрос с индексом выполняется быстрее
    assert duration_with_index < duration_no_index, "Запрос с индексом выполняется дольше, чем без индекса"

def test_performance_select_like_index_last_2(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string9____'"

    # Выполнение запроса без индекса
    start_time_no_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_no_index = time.time() - start_time_no_index

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Выполнение запроса с индексом
    start_time_with_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_with_index = time.time() - start_time_with_index

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    cursor.close()

    # Вывод времени с выполнением запросов
    print(f"\nВремя выполнения запроса с индексом: {duration_with_index:.6f} секунд")
    print(f"Время выполнения запроса без индекса: {duration_no_index:.6f} секунд")

    # Проверка, что запрос с индексом выполняется быстрее
    assert duration_with_index < duration_no_index, "Запрос с индексом выполняется дольше, чем без индекса"

def test_performance_select_like_index_last_3(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string7___7'"

    # Выполнение запроса без индекса
    start_time_no_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_no_index = time.time() - start_time_no_index

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Выполнение запроса с индексом
    start_time_with_index = time.time()
    cursor.execute(query)
    cursor.fetchall()
    duration_with_index = time.time() - start_time_with_index

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    cursor.close()

    # Вывод времени с выполнением запросов
    print(f"\nВремя выполнения запроса с индексом: {duration_with_index:.6f} секунд")
    print(f"Время выполнения запроса без индекса: {duration_no_index:.6f} секунд")

    # Проверка, что запрос с индексом выполняется быстрее
    assert duration_with_index < duration_no_index, "Запрос с индексом выполняется дольше, чем без индекса"