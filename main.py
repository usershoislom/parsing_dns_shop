import os

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.endpoints import tasks
from app.core.templates import templates
from app.core.datastore import init_db

app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app/templates"))
# print(BASE_DIR)
# set_templates(templates)
init_db()
app.include_router(tasks.router)

# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     print("in index")
#     return templates.TemplateResponse("index.html", {"request": request})



