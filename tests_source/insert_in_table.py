import mysql.connector
from mysql.connector import errorcode

try:
    # Подключение к базе данных
    cnx = mysql.connector.connect(
        user='mysql_user',
        password='Qq123456!',
        host='localhost',
        database='test'
    )
    cursor = cnx.cursor()

    # Вставка строк в таблицу test_table
    insert_query = """
    INSERT INTO test_table (str) VALUES (%s);
    """
    for i in range(1, 100001):
        str = f'string{i}'
        cursor.execute(insert_query, (str,))

    # Фиксация изменений
    cnx.commit()
    print("Cтроки вставлены в таблицу test_table")

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Ошибка доступа: Неправильное имя пользователя или пароль")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Ошибка: База данных не существует")
    else:
        print(err)
else:
    cnx.close()
