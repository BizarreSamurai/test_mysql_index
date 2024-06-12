# Отчёт по тестированию индексов на MySQL
## 1. Описание стенда
- Тестирование проводилось на __MySQL  Ver 8.0.36-0ubuntu0.22.04.1 for Linux on x86_64 ((Ubuntu))__
- Для подключение к БД использовалась Python библиотека __mysql.connector__
- Тестовая таблица представляет собой один столбец __str__ с типом данных __VARCHAR(255)__ на __100 000__ записей: от ___string1___ до ___string100000___

## 2. Описание кода проекта тестирования
Проект представляет собой:
- функциональные тесты (functional_tests.py)
- перфоманс тесты (perfomance_tests.py, index_not_used.py)
- скрипт создания таблицы (create_table.py)
- скрипт по наполнению таблицы (insert_in_table.py)
- скрипт по автоматизации создания и наполнения таблицы (create_insert_table.py) (по сути он просто запускает предыдущие два скрипта)
- скрипт для удаления таблицы (drop_table.py) (просто выполняет DROP TABLE test_table)
- cкрипт по для запуска функциональных и перфоманс тестов и вывода их результатов в консоль (run_tests.py)

По сути для работы уже было достаточно первых четырёх скриптов (они находятся в папке tests_source), но для удобства процесса работы я написал ещё эти три.

## 3. Тесты
### 3.1 Функциональные тесты

> Написать функциональные тесты на SELECT str like pattern.
> Нужно убедиться, что результаты работы запросов на одинаковых данных не отличаются, 
> когда на колонке str нет индекса и когда он есть.

Как функциональный тест не крути результат один и тот же, что и следавало ожидать.
Тестировалось на трёх запросах:
- SELECT * FROM test_table WHERE str LIKE 'string77777'
- SELECT * FROM test_table WHERE str LIKE 'string9____'
- SELECT * FROM test_table WHERE str LIKE 'string7___7'

Пример вывода результата теста в консоль:
```sh
samurai@mysql:~/test_mysql_index$ pytest -s -v tests_source/functional_tests.py 
==================================== test session starts ==================================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collected 3 items                                                                                                                                    

tests_source/functional_tests.py::test_functional_select_like_1 PASSED
tests_source/functional_tests.py::test_functional_select_like_2 PASSED
tests_source/functional_tests.py::test_functional_select_like_3 PASSED

==================================== 3 passed in 0.77s  ==================================
```

### 3.2 Перфоманс тесты

> Написать перфоманс тесты на SELECT str like pattern.
> Нужно убедиться, что запросы с использованием индексов работают быстрее, чем без них.
> Найти и показать случай, когда индекс не будет использоваться.
> Проект нужно написать на Python3 с использованием pytest.

Тестирование производительности проводилось на аналогичных запросах, что и в фунциональных тестах, но также было протестированно как влияет на время выполнения запросов последовательность выполнения запроса с индексом и без индекса (в запрос было добавлено SQL_NO_CACHE, чтобы исключить использование кэша):
- SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string77777'
- SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string9____'
- SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE 'string7___7'

Пример вывода результата теста в консоль:
```sh
samurai@mysql:~/test_mysql_index$ pytest -s -v tests_source/perfomance_tests.py 
================================= test session starts =====================================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collected 6 items                                                                                                                                    

tests_source/perfomance_tests.py::test_performance_select_like_index_first_1 
Время выполнения запроса с индексом: 0.000566 секунд
Время выполнения запроса без индекса: 0.031216 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_first_2 
Время выполнения запроса с индексом: 0.009952 секунд
Время выполнения запроса без индекса: 0.035932 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_first_3 
Время выполнения запроса с индексом: 0.006818 секунд
Время выполнения запроса без индекса: 0.033908 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_1 
Время выполнения запроса с индексом: 0.000349 секунд
Время выполнения запроса без индекса: 0.031909 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_2 
Время выполнения запроса с индексом: 0.016881 секунд
Время выполнения запроса без индекса: 0.040490 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_3 
Время выполнения запроса с индексом: 0.007023 секунд
Время выполнения запроса без индекса: 0.035272 секунд
PASSED

=================================== 6 passed in 1.50s =====================================
```
Наглядно видно, что использование индекса в данных запросах помогает ускорить время выполнения до 5 раз, но такой наглядный результат был достигнут на таблице со 100 000 записей. Чем меньше записей в таблице, тем меньше разница в скорости выполнения, но всё же запросы с индексом выполняются побыстрее.
Пример выполнения теста на таблице с 1000 записей (благодаря скрипту автоматизации удобно играться с количеством записей):
```sh
samurai@mysql:~/test_mysql_index$ pytest -s -v tests_source/perfomance_tests.py 
================================== test session starts ====================================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collected 6 items                                                                                                                                    

tests_source/perfomance_tests.py::test_performance_select_like_index_first_1 
Время выполнения запроса с индексом: 0.000469 секунд
Время выполнения запроса без индекса: 0.000540 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_first_2 
Время выполнения запроса с индексом: 0.000384 секунд
Время выполнения запроса без индекса: 0.000552 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_first_3 
Время выполнения запроса с индексом: 0.000343 секунд
Время выполнения запроса без индекса: 0.000529 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_1 
Время выполнения запроса с индексом: 0.000253 секунд
Время выполнения запроса без индекса: 0.000486 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_2 
Время выполнения запроса с индексом: 0.000366 секунд
Время выполнения запроса без индекса: 0.000526 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_3 
Время выполнения запроса с индексом: 0.000412 секунд
Время выполнения запроса без индекса: 0.000672 секунд
PASSED

==================================== 6 passed in 0.16s ====================================
```
Теперь разница в скороси выполнения не такая заметная.

Рассмотрим случаи, когда при запросе индекс не будет использоваться:
- SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE '%77777'
- SELECT SQL_NO_CACHE * FROM test_table WHERE LOWER(str) LIKE 'string77777'

Когда строка начинается с %, MySQL не может использовать индекс для ускорения поиска, так как % означает, что перед 77777 может быть любое количество символов. В результате, MySQL вынужден выполнить полное сканирование таблицы (full table scan), чтобы найти соответствующие строки.

Индексы в MySQL хранят данные в исходном виде и не могут быть использованы для запросов, которые включают функции, трансформирующие значения столбцов (например, LOWER, UPPER, TRIM, и т.д.). Когда в запросе используются такие функции, то MySQL должен применить их ко всем строкам таблицы перед выполнением сравнения, что также приводит к полному сканированию таблицы.

В самом тесте будем смотреть на столбец __possible_keys__ при выполнении вышеуказанных запросов с впередистоящим __EXPLAIN__.

Пример выполнения теста:
```sh
samurai@mysql:~/test_mysql_index$ pytest -s -v tests_source/index_not_used.py 
================================== test session starts ====================================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collected 2 items                                                                                                                                    

tests_source/index_not_used.py::test_index_not_used_1 
Использование индекса в запросе SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE '%77777': False
PASSED
tests_source/index_not_used.py::test_index_not_used_2 
Использование индекса в запросе SELECT SQL_NO_CACHE * FROM test_table WHERE LOWER(str) LIKE 'string77777': False
PASSED

==================================== 2 passed in 0.42s ====================================
```
## 4. Запуск проекта
Чтобы проверить работоспособность проекта, достаточно иметь заранее установленную MySQL с созданной базой данных test и пользователем mysql_user, имеющим права на всё в test и установленным паролем 'Qq123456!':
- user='mysql_user', 
- password='Qq123456!', 
- host='localhost', (сам проект запускался там же, где стоит MySQL)
- database='test'

Для запуска проекта запускаем поледовательно два скрипта (create_insert_table.py и run_tests.py):
### create_insert_table.py:
```sh
samurai@mysql:~/test_mysql_index$ python3 create_insert_table.py 
Command python3 tests_source/create_table.py executed successfully.
Output:
Таблица создана успешно.

Command python3 tests_source/insert_in_table.py executed successfully.
Output:
Cтроки вставлены в таблицу test_table
```
### run_tests.py:
```sh
samurai@mysql:~/test_mysql_index$ python3 run_tests.py 
Command pytest -s -v tests_source/functional_tests.py executed.
Output:
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collecting ... collected 3 items

tests_source/functional_tests.py::test_functional_select_like_1 PASSED
tests_source/functional_tests.py::test_functional_select_like_2 PASSED
tests_source/functional_tests.py::test_functional_select_like_3 PASSED

============================== 3 passed in 0.73s ===============================

Command pytest -s -v tests_source/perfomance_tests.py executed.
Output:
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collecting ... collected 6 items

tests_source/perfomance_tests.py::test_performance_select_like_index_first_1 
Время выполнения запроса с индексом: 0.000417 секунд
Время выполнения запроса без индекса: 0.032520 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_first_2 
Время выполнения запроса с индексом: 0.009482 секунд
Время выполнения запроса без индекса: 0.036463 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_first_3 
Время выполнения запроса с индексом: 0.007048 секунд
Время выполнения запроса без индекса: 0.032652 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_1 
Время выполнения запроса с индексом: 0.000336 секунд
Время выполнения запроса без индекса: 0.030634 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_2 
Время выполнения запроса с индексом: 0.015639 секунд
Время выполнения запроса без индекса: 0.035157 секунд
PASSED
tests_source/perfomance_tests.py::test_performance_select_like_index_last_3 
Время выполнения запроса с индексом: 0.007306 секунд
Время выполнения запроса без индекса: 0.040586 секунд
PASSED

============================== 6 passed in 1.42s ===============================

Command pytest -s -v tests_source/index_not_used.py executed.
Output:
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/samurai/test_mysql_index
collecting ... collected 2 items

tests_source/index_not_used.py::test_index_not_used_1 
Использование индекса в запросе SELECT SQL_NO_CACHE * FROM test_table WHERE str LIKE '%77777': False
PASSED
tests_source/index_not_used.py::test_index_not_used_2 
Использование индекса в запросе SELECT SQL_NO_CACHE * FROM test_table WHERE LOWER(str) LIKE 'string77777': False
PASSED

============================== 2 passed in 0.43s ===============================
```
Таким образом получаем проверку всех тестов в один клик)
Удалить таблицу можно с помощью скрипта drop_table.py (по сути он выполняет только DROP TABLE test_table, но зато не надо заходить в сам MySQL при работе с тестами).
### drop_table.py:
```sh
samurai@mysql:~/test_mysql_index$ python3 drop_table.py 
Таблица успешно удалена
```
Вот так вот всё удобненько. Если хочется посмотреть тесты по отдельности, то сделать это можно запуская отдельно тесты functional_tests.py, perfomance_tests.py, index_not_used.py (для более подробного выввода в pytest можно использовать ключи -s -v). Аналогично для таблиц используются скрипты create_table.py и insert_in_table.py, если хочется поиграться со структурой таблицы и данными для наполнения.
## 5. Вывод
Все поставленные задачи тестового задания были выполнены и наглядно продемонстрированы. Здорово же получилось) Хотелось бы поработать с вами вместе ;)
