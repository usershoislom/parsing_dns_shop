import os
from fastapi.templating import Jinja2Templates

# Определяем путь относительно корня проекта
TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def get_templates():
    print("in get_templates")
    return templates
