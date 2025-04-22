import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, random
from bs4 import BeautifulSoup


def extract_total_pages(html):
    soup = BeautifulSoup(html, "html.parser")

    last_page_link = soup.find('a', class_='pagination-widget__page-link_last')

    last_page = last_page_link['href'].split("=")[-1]
    return int(last_page)

def get_html_page(url):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-blink-features")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options, headless=False, use_subprocess=True, version_main=135)

    all_links = []

    try:
        driver.set_page_load_timeout(random.randint(30, 60))
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".catalog-product.ui-button-widget"))
        )

        total_pages = extract_total_pages(driver.page_source)
        print(f"Всего страниц: {total_pages}")

        for page_number in range(1, total_pages + 1):
            page_url = f"{url}?p={page_number}"
            print(f"\nПарсим страницу {page_number}: {page_url}")
            driver.get(page_url)

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".catalog-product.ui-button-widget"))
            )

            time.sleep(random.uniform(1, 3))  # Подождем чуть для подгрузки

            html = driver.page_source
            links = extract_product_links(html)
            all_links.extend(links)
            print(f"На странице {page_number} найдено {len(links)} ссылок")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.quit()

    return all_links


def extract_product_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    product_containers = soup.find_all('a', class_='catalog-product__name ui-link ui-link_black')
    product_links = [container.get('href') for container in product_containers]
    return product_links


links = get_html_page("https://www.dns-shop.ru/catalog/17a8a69116404e77/myshi/")
print(f"\nОбщее количество ссылок: {len(links)}")

















# import undetected_chromedriver as uc
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# import time, random
#
# from bs4 import BeautifulSoup
#
#
# def get_html_page(url):
#     options = uc.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-infobars")
#     options.add_argument("--start-maximized")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
#
#     # Добавляем дополнительные опции для лучшей маскировки
#     options.add_argument("--disable-popup-blocking")
#     options.add_argument("--disable-notifications")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-web-security")
#     options.add_argument("--disable-features=IsolateOrigins,site-per-process")
#     options.add_argument("--disable-blink-features")
#
#     driver = uc.Chrome(
#         options=options,
#         headless=False,
#         use_subprocess=True,
#         version_main=135
#     )
#
#     try:
#         driver.set_page_load_timeout(random.randint(30, 60))
#
#         driver.get(url)
#
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
#         )
#
#         # Имитируем человеческое поведение
#         # actions = ActionChains(driver)
#         # for _ in range(5):
#         #     # Плавные перемещения курсора
#         #     x_offset = random.randint(0, 20)
#         #     y_offset = random.randint(0, 20)
#         #     actions.move_by_offset(x_offset, y_offset).perform()
#         #     time.sleep(random.uniform(0.5, 1.5))
#         #
#         # # Прокрутка страницы с паузами
#         # scroll_pauses = [random.randint(10, 20) for _ in range(8)]
#         # for pause in scroll_pauses:
#         #     driver.execute_script(f"window.scrollBy(0, {pause});")
#         #     time.sleep(random.uniform(0.8, 2.5))
#
#         # Дополнительное ожидание для подгрузки товаров
#         # time.sleep(3)
#
#         # Явное ожидание появления карточек товаров
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".catalog-product.ui-button-widget")))
#
#         # Получаем и выводим количество найденных товаров
#         products = driver.find_elements(By.CSS_SELECTOR, ".catalog-product.ui-button-widget")
#         print(f"Найдено {len(products)} карточек товаров")
#
#         # Сохраняем HTML для проверки
#         with open("dns_shop_page.html", "w", encoding="utf-8") as f:
#             f.write(driver.page_source)
#
#         extract_product_links(driver.page_source)
#     except Exception as e:
#         print(f"Произошла ошибка: {str(e)}")
#         with open("dns_shop_error_page.html", "w", encoding="utf-8") as f:
#             f.write(driver.page_source)
#     finally:
#         driver.quit()
#
#
# def extract_product_links(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     product_containers = soup.find_all('a', class_='catalog-product__name ui-link ui-link_black')
#     product_links = []
#     for i, container in enumerate(product_containers):
#         product_links.append(container.get('href'))
#         print(i, container.get('href'))
#
#     return product_links
#
#
# print(get_html_page("https://www.dns-shop.ru/catalog/17a8a69116404e77/myshi/"))
