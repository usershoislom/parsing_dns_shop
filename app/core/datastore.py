import sqlite3
import traceback

DB_NAME = "products.db"


def init_db():
    print("in init_db")
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_links(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE
            )
        ''')
        conn.commit()
    except Exception:
        print(traceback.format_exc())
    finally:
        if conn:
            conn.close()


def insert_into_db(urls: list):
    print("in insert_into_db")
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.executemany('''
        INSERT OR IGNORE INTO product_links (url)
        VALUES (?)
        ''', [(url,) for url in urls])
        conn.commit()
    except Exception:
        print(traceback.format_exc())
    finally:
        if conn:
            conn.close()


def get_all_urls_from_db() -> list[str]:
    print("in get_all_urls_from_db")
    conn = None
    urls = []
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT url FROM product_links
        ''')
        urls = [row[0] for row in cursor.fetchall()]
    except Exception:
        print(traceback.format_exc())
    finally:
        if conn:
            conn.close()

    return urls

# import os
# import pandas as pd
#
#
# class DataStore:
#     def __init__(self):
#         if os.path.exists("all_links.xlsx"):
#             self.data = pd.read_excel("all_links.xlsx", engine="openpyxl")
#         else:
#             self.data = pd.DataFrame(columns=["urls"])
#
#     def get_data(self):
#         return self.data
#
#     def update_data(self, new_data: pd.DataFrame):
#         self.data = new_data
#         new_data.to_excel("all_links.xlsx", index=False)
#
#
# datastore = DataStore()