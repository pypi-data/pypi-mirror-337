from igorskis_framework.config import TEMPLATE_FILES
import os

def create_project(project_name):
    """Создаёт новый проект с базовой структурой."""
    if os.path.exists(project_name):
        print(f"Ошибка: Папка '{project_name}' уже существует.")
        return

    os.makedirs(project_name)  # Создаём папку проекта
    os.makedirs(os.path.join(project_name, "static"))  # Создаём папку для статических файлов
    os.makedirs(os.path.join(project_name, "db"))  # Создаём папку для базы данных
    os.makedirs(os.path.join(project_name, "html"))  # Создаём папку для шаблонов

    for filename, content in TEMPLATE_FILES.items():
        file_path = os.path.join(project_name, filename)
        with open(file_path, "w") as f:
            f.write(content)

    print(f"Проект '{project_name}' успешно создан!")


def run_project(debug=False):
    print("Запуск проекта...")

    if debug:
        print("Включен режим отладки.")
        print("Сервер запущен в режиме отладки.")
        print("Перезапуск сервера при изменении Python-файлов.")
        os.system("python manage.py")
    elif debug == False:
        print("Включен режим продакшена.")
        print("Сервер запущен в режиме продакшена.")
        os.system("python server.py")
