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

    # Удаление таблицы
    cursor.execute("DROP TABLE test_table")
    print("Таблица успешно удалена")

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