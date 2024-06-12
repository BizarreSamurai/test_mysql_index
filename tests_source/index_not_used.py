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

def execute_query(cursor, query):
    cursor.execute(query)
    cursor.fetchall()

def check_index_usage(cursor, query):
    cursor.execute(f"EXPLAIN {query}")
    explain_result = cursor.fetchall()
    # Проверка, используется ли индекс
    used_indexes = [row[5] for row in explain_result]
    return any(used_indexes)

def test_index_not_used_1(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE '%77777'"

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Проверка использования индекса
    index_used = check_index_usage(cursor, query)
    print(f'\nИспользование индекса в запросе {query}: {index_used}')
    
    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")

    assert not index_used, "Индекс не должен был быть использован, но был."

    cursor.close()


def test_index_not_used_2(db_connection):
    cursor = db_connection.cursor()

    query = "SELECT SQL_NO_CACHE * FROM test_table WHERE LOWER(str) LIKE 'string77777'"

    # Создание индекса
    cursor.execute("CREATE INDEX index_str ON test_table (str)")

    # Проверка использования индекса
    index_used = check_index_usage(cursor, query)
    print(f'\nИспользование индекса в запросе {query}: {index_used}')

    # Удаление индекса
    cursor.execute("DROP INDEX index_str ON test_table")
    
    assert not index_used, "Индекс не должен был быть использован, но был."

    cursor.close()
