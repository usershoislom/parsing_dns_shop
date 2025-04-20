import threading
from app.scraping.parser import save_all_product_links

lock = threading.Lock()
first_run_done = False


def run_once_on_startup():
    global first_run_done
    if not first_run_done:
        with lock:
            if not first_run_done:
                print("Выполняем первое обновление при старте")
                save_all_product_links()
                first_run_done = True
            else:
                print("Уже запускалось, пропускаем")
