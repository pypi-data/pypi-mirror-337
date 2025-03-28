from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time
from webdriver_manager.chrome import ChromeDriverManager
import json

def getinfo(url: str) -> dict:
    """
    Получает информацию о товаре с Wildberries по URL, используя полные XPath.
    Браузер остаётся открытым до ручного подтверждения (Enter).
    Ожидает загрузки всех необходимых элементов.
    """
    
    # Настройка Chrome (видимый режим + отключение авто-закрытия)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Режим без графического интерфейса
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
#    chrome_options.add_experimental_option("detach", True)  # Браузер не закроется автоматически
    
    try:
        # Проверка URL
        if not urlparse(url).netloc.endswith('wildberries.ru'):
            return {"error": "Invalid Wildberries URL"}

        # Инициализация драйвера
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        
        # Ожидание загрузки основных элементов
        wait = WebDriverWait(driver, 20)  # Максимальное время ожидания 20 секунд
        
        # Словарь с XPath для всех нужных элементов
        elements_xpath = {
            "name": '/html/body/div[1]/main/div[2]/div[2]/div[3]/div/div[3]/div[9]/div[1]/h1',
            "price": '/html/body/div[1]/main/div[2]/div[2]/div[3]/div/div[3]/div[14]/div/div[1]/div[1]/div/div/div/p/span/ins',
            "brand": '/html/body/div[1]/main/div[2]/div[2]/div[3]/div/div[3]/div[9]/div[1]/div/a',
            "rating": '/html/body/div[1]/main/div[2]/div[2]/div[3]/div/div[3]/div[9]/div[2]/a[1]/span[1]'
        }
        
        # Ожидаем появления каждого элемента
        for element in elements_xpath.values():
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, element)))
            except Exception as e:
                print(f"Элемент не найден: {element}. Ошибка: {str(e)}")
        
        # Извлечение данных по оригинальным XPath
        data = {
            "name": safe_extract(driver, elements_xpath["name"]),
            "price": clean_price(safe_extract(driver, elements_xpath["price"])),
            "brand": safe_extract(driver, elements_xpath["brand"]),
            "rating": safe_extract(driver, elements_xpath["rating"]),
            "product_id": url.split('/')[-2],
            "url": url
        }

        if not any(data.values()):
            return {"error": "No data found (page structure changed)"}

        return data

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
    finally:
        try:
            driver.quit()  # Закрытие по команде
        except:
            pass

def safe_extract(driver, xpath: str, default: str = "") -> str:
    """Безопасное извлечение текста по XPath"""
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.text.strip()
    except:
        return default

def clean_price(price_str: str) -> str:
    """Очистка строки с ценой. Возвращает число в виде строки или '0' при ошибке."""
    if not price_str:
        return "0"
    
    # Удаляем все нецифровые символы, кроме точки и запятой (для десятичных разделителей)
    cleaned = ''.join(c for c in price_str if c.isdigit() or c in {'.', ','})
    
    # Заменяем запятую на точку, если есть (для float конверсии)
    cleaned = cleaned.replace(',', '.')
    
    try:
        # Пробуем преобразовать в float, затем округляем до целого
        price_num = float(cleaned)
        return str(int(round(price_num)))
    except (ValueError, TypeError):
        return "0"