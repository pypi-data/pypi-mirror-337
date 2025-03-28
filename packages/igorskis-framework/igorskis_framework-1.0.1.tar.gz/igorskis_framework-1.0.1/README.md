# Igorskis Framework

Igorskis Framework — это веб-фреймворк для создания веб-приложений.

Чтобы создать веб-приложение, ты можешь использовать команду:
```sh
igorskis-admin startproject project_name
```

### Определение маршрутов
Ты можешь создавать URL-адреса в `urls.py` командой:
```python
router.add_route(path, view)
```

### Контроллеры (views)
В `views.py` можно создавать функции для рендеринга страниц. Пример:
```python
def index():
    return html("index.html")
```
Создай файл `html/index.html` и добавь в него HTML-код.

Также можно передавать параметры в функцию `html`. Пример:
```python
html("index.html", name="John Doe")
```
В таком случае в `html/index.html` ты можешь использовать переменную `name` так:
```html
{{ name }}
```

### Работа с моделями
В `models.py` можно создавать модели. Пример:
```python
class User(Model):
    def __init__(self, name, email):
        super().__init__(name=name, email=email)
```
В моделях можно использовать методы:
- `get_all()`
- `update()`
- `delete()`

Чтобы создать экземпляр модели:
```python
user = User(name="John Doe", email="9K9bM@example.com")
```
Чтобы добавить экземпляр модели в базу данных, вызови метод:
```python
user.save()
```

### Статические файлы
Картинки, CSS-стили и JavaScript-скрипты добавляются в папку `static/`.

### Запуск сервера
Для разработки используй команду:
```sh
python3 manage.py
```
Для продакшена используй команду:
```sh
python3 server.py
```
### Что нового в версии 1.0.1
- Добавлен CORS.
- Добавлен файл `settings.py` с настройками. (Пока настраивается только `STATIC_URL`. Эта настройка нужна для обслуживания статических файлов.)
