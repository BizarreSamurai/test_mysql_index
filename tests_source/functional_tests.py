import pytest
import mysql.connector

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

def test_functional_select_like_1(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT * FROM test_table WHERE str LIKE 'string77777'"
    
    # Запрос без индекса
    cursor.execute(query)
    result_no_index = cursor.fetchall()

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")
    
    # Запрос с индексом
    cursor.execute(query)
    result_with_index = cursor.fetchall()
    
    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    cursor.close()
    
    assert result_no_index == result_with_index, "Результаты запросов с и без индекса не совпадают"

def test_functional_select_like_2(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT * FROM test_table WHERE str LIKE 'string9____'"
    
    # Запрос без индекса
    cursor.execute(query)
    result_no_index = cursor.fetchall()

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")
    
    # Запрос с индексом
    cursor.execute(query)
    result_with_index = cursor.fetchall()
    
    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    cursor.close()
    
    assert result_no_index == result_with_index, "Результаты запросов с и без индекса не совпадают"

def test_functional_select_like_3(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT * FROM test_table WHERE str LIKE 'string7___7'"
    
    # Запрос без индекса
    cursor.execute(query)
    result_no_index = cursor.fetchall()

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")
    
    # Запрос с индексом
    cursor.execute(query)
    result_with_index = cursor.fetchall()
    
    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    cursor.close()
    
    assert result_no_index == result_with_index, "Результаты запросов с и без индекса не совпадают"