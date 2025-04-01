import argparse

from igorskis_framework.cli_functions import *
from igorskis_framework.help_functions import *

def main():
    parser = argparse.ArgumentParser(description="Igorskis Framework CLI")
    parser.add_argument("command", help="Команда (например, 'startproject' или 'runproject')")
    parser.add_argument("project_name_or_debug", help="Название проекта или флаг отладки")

    args = parser.parse_args()

    if args.command == "startproject":
        create_project(args.project_name_or_debug)
    elif args.command == "runproject":
        debug = convert_to_bool(args.project_name_or_debug)
        run_project(debug)
    else:
        print("Неизвестная команда. Используйте: igorskis-admin startproject [project-name] или igorskis-admin runproject [debug]")


if __name__ == "__main__":
    main()
