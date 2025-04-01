from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Настройка Jinja2 для загрузки шаблонов из папки "html"
env = Environment(loader=FileSystemLoader("html"))

def html(template_name, **context):
    """Функция для рендеринга HTML-шаблонов с переданными параметрами."""
    try:
        template = env.get_template(template_name)  # Загружаем шаблон
        return template.render(**context)  # Рендерим с параметрами
    except TemplateNotFound:
        return f"Ошибка: Шаблон '{template_name}' не найден."
    except Exception as e:
        return f"Ошибка при рендеринге шаблона: {str(e)}"
