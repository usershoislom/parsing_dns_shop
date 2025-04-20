import threading
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse
from app.core.templates import templates
from app.core.startup import run_once_on_startup
from app.scraping.parser import get_items_urls_by_category

router = APIRouter()


@router.on_event("startup")
def start_background_task():
    threading.Thread(target=run_once_on_startup).start()


@router.get("/")
async def index(request: Request):
    context = {
        "request": request,
        "title": "Главная страница"
    }
    print("in index")
    return templates.TemplateResponse("index.html", context)


@router.get("/download")
async def get_products_by_category(request: Request):
    print("in get products")
    products_path = get_items_urls_by_category("smartfon")
    print("got products urls")
    return FileResponse(products_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# @router.post("/update")
# async def update_database(request: Request, templates=Depends(get_templates)):
#     new_data = save_all_product_links()
#     datastore.update_data(new_data)
#     return RedirectResponse("/", status_code=303)