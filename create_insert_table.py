import subprocess
import os
import platform

def run_script(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f'Command {" ".join(command)} executed successfully.')
        print(f'Output:\n{result.stdout}')
    except subprocess.CalledProcessError as e:
        print(f'Command {" ".join(command)} failed.')
        print(f'Error:\n{e.stderr}')

python_executable = 'python3' if platform.system() != 'Windows' else 'python'

scripts_python3 = [
    os.path.join('tests_source', 'create_table.py'),  # скрипт для создания таблицы
    os.path.join('tests_source', 'insert_in_table.py')   # скрипт для вставки записей
]

# Запуск скриптов через python3 или python
for script in scripts_python3:
    run_script([python_executable, script])