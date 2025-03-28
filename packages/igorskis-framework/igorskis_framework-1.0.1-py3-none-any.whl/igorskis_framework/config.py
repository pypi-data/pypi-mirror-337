TEMPLATE_FILES = {
    "manage.py": '''import time
from watchdog.observers import Observer
from igorskis_framework.restart_handler import RestartHandler

if __name__ == "__main__":
    print("[INFO] Автоперезапуск сервера активирован...")
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n[INFO] Остановка сервера.")
        event_handler.server_process.terminate()
        observer.stop()

    observer.join()
''',

    "server.py": '''from igorskis_framework.middlewares.static_files import serve_static_file
from wsgiref.simple_server import make_server
from igorskis_framework.router import router
from igorskis_framework.middlewares.cors import CORS
from settings import STATIC_URL
import urls  # Загружаем маршруты

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    
    # Если путь начинается с /static/, обслуживаем статический файл
    if path.startswith(STATIC_URL):
        file_data = serve_static_file(path)
        if file_data:
            status = "200 OK"
            # Определяем тип контента в зависимости от расширения
            if path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "application/octet-stream"
            
            headers = [("Content-Type", content_type), ("Content-Length", str(len(file_data)))]
            start_response(status, headers)
            return [file_data]
        else:
            status = "404 Not Found"
            response_body = b"<h1>File not found</h1>"
            headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]
            start_response(status, headers)
            return [response_body]
    
    # Для обычных маршрутов
    view, params = router.resolve(path)
    
    if view:
        response_body = view(**params).encode("utf-8")
        status = "200 OK"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]
    else:
        response_body = b"<h1>404 Not Found</h1>"
        status = "404 Not Found"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]

    start_response(status, headers)
    return [response_body]


app = CORS(application)

if __name__ == "__main__":
    with make_server("", 8000, app) as server:
        print("Serving on port 8000...")
        server.serve_forever()
''',

    "urls.py": '''from igorskis_framework.router import router
from views import *''',

    "views.py": '''from igorskis_framework.templates import html''',
    "models.py": '''from igorskis_framework.models import Model''',
    "settings.py": '''STATIC_URL = "/static/"''',
    "__init__.py": ''''''
}
