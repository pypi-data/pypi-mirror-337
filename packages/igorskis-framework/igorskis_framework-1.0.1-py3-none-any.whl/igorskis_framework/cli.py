import os
import argparse

from igorskis_framework.config import TEMPLATE_FILES


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


def main():
    parser = argparse.ArgumentParser(description="Igorskis Framework CLI")
    parser.add_argument("command", help="Команда (например, 'startproject')")
    parser.add_argument("project_name", help="Название проекта")

    args = parser.parse_args()

    if args.command == "startproject":
        create_project(args.project_name)
    else:
        print("Неизвестная команда. Используйте: igorskis-admin startproject project-name")


if __name__ == "__main__":
    main()
