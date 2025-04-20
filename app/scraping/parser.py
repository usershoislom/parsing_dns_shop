import requests
import pandas as pd
import xml.etree.ElementTree as ET

from app.core.datastore import insert_into_db, get_all_urls_from_db

headers = {"User-Agent": "Mozilla/5.0"}

NS = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

DNS_SITEMAP_URL = "https://www.dns-shop.ru/sitemap.xml"


def save_all_product_links(sitemap_index_url: str = DNS_SITEMAP_URL):
    print("Collecting all links")
    resp = requests.get(sitemap_index_url, headers=headers)
    root = ET.fromstring(resp.text)

    sitemap_urls = [el.find('ns:loc', NS).text for el in root.findall('ns:sitemap', NS)]
    all_products_urls = []
    i = 0
    for sitemap_url in sitemap_urls:
        r = requests.get(sitemap_url, headers=headers)
        sub_root = ET.fromstring(r.text)

        all_products_urls += [url.find("ns:loc", NS).text for url in sub_root.findall('ns:url', NS)]

        # insert_into_db(all_products_urls)
        print(f"{i} тая итерация получения ссылок с sitemap")
        i += 1

    print(f"Всего собрано {len(all_products_urls)} ссылок, записываем в базу...")
    insert_into_db(all_products_urls)
    print("✅ Все ссылки записаны")


# def get_all_links():
#     df = pd.read_excel("all_links.xlsx", engine="openpyxl")
#     links = df["urls"].tolist()
#     return links


def get_items_urls_by_category(category_name: str):
    print("int get_items_urls_by_category")
    items = []
    all_urls = get_all_urls_from_db()
    for product_url in all_urls:
        if category_name in product_url:
            items.append(product_url)

    df = pd.DataFrame(items, columns=[category_name])
    path = f"{category_name}.xlsx"
    df.to_excel(path, index=False)

    return path
