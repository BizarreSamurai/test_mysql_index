import subprocess
import os

def run_script(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(f'Command {" ".join(command)} executed.')
        print(f'Output:\n{result.stdout}')
        if result.returncode != 0:
            print(f'Error:\n{result.stderr}')
    except Exception as e:
        print(f'Failed to execute command {" ".join(command)}.')
        print(f'Error: {str(e)}')

scripts_pytest = [
    os.path.join('tests_source', 'functional_tests.py'),  # функциональный тест
    os.path.join('tests_source', 'perfomance_tests.py'),  # тест производительности с индексом
    os.path.join('tests_source', 'index_not_used.py')   # тест производительности с индексом, где индекс не используется при обработке запроса
]

# Запуск скриптов через pytest с флагами для подробного вывода
for script in scripts_pytest:
    run_script(['pytest', '-s', '-v', script])
